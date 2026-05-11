/*
 * gemm_poc.c
 *
 * Advanced standalone double-precision GEMM portability kernel.
 *
 * This file is inspired by the architectural ideas explored in:
 *   crissmath/Gemm_Evaluation
 *   https://github.com/crissmath/Gemm_Evaluation.git
 *
 * The goal is not to depend on BLAS/OpenBLAS/MKL yet, but to provide a
 * portable, dependency-free FP64 kernel that can be compiled natively and
 * cross-compiled for RISC-V.
 *
 * Implemented kernels:
 *   1. Inner Product GEMM  : baseline, cache-unfriendly reference.
 *   2. Outer Product GEMM  : rank-1 update formulation, better locality.
 *   3. Blocked Outer GEMM  : simple cache-aware extension.
 *
 * Validation:
 *   The program compares the numerical results of the three kernels and
 *   prints deterministic metrics that can be compared across x86_64 and
 *   RISC-V/QEMU execution.
 */

#include <errno.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define IDX(i, j, ld) ((size_t)(j) * (size_t)(ld) + (size_t)(i))

static int parse_size(int argc, char **argv)
{
    if (argc < 2)
    {
        return 64;
    }

    errno = 0;
    char *endptr = NULL;
    long value = strtol(argv[1], &endptr, 10);

    if (errno != 0 || endptr == argv[1] || *endptr != '\0')
    {
        fprintf(stderr, "ERROR: invalid matrix size: %s\n", argv[1]);
        exit(EXIT_FAILURE);
    }

    if (value < 2 || value > 512)
    {
        fprintf(stderr, "ERROR: matrix size must be between 2 and 512.\n");
        exit(EXIT_FAILURE);
    }

    return (int)value;
}

static void initialize_matrices(int n, double *A, double *B)
{
    /*
     * Deterministic initialization.
     *
     * No random numbers are used because the goal is reproducible numerical
     * validation across native and RISC-V execution.
     *
     * Matrices are stored in column-major layout:
     *
     *     element(i, j) = buffer[j * leading_dimension + i]
     */
    const int ld = n;

    for (int j = 0; j < n; ++j)
    {
        for (int i = 0; i < n; ++i)
        {
            const int aval = (((i + 1) * (j + 3) + 7) % 29) - 14;
            const int bval = (((i + 5) + (j + 2) * 7) % 31) - 15;

            A[IDX(i, j, ld)] = ((double)aval / 29.0) + ((i == j) ? 1.0 : 0.0);

            B[IDX(i, j, ld)] = ((double)bval / 31.0) + (((i + j) % 5 == 0) ? 0.125 : 0.0);
        }
    }
}

static void zero_matrix(int n, double *C)
{
    memset(C, 0, (size_t)n * (size_t)n * sizeof(double));
}

static void gemm_inner_product(int n, const double *A, const double *B, double *C)
{
    /*
     * Baseline inner-product GEMM:
     *
     *     C(i,j) = sum_p A(i,p) * B(p,j)
     *
     * This mirrors the classical dot-product formulation. In column-major
     * storage, the access to A(i,p) across p is strided, which is useful as a
     * baseline for portability and locality discussion.
     */
    const int ld = n;

    for (int j = 0; j < n; ++j)
    {
        for (int i = 0; i < n; ++i)
        {
            double sum = 0.0;

            for (int p = 0; p < n; ++p)
            {
                sum += A[IDX(i, p, ld)] * B[IDX(p, j, ld)];
            }

            C[IDX(i, j, ld)] = sum;
        }
    }
}

static void gemm_outer_product(int n, const double *A, const double *B, double *C)
{
    /*
     * Outer-product / rank-1 update GEMM:
     *
     *     C = sum_p A(:,p) * B(p,:)
     *
     * For column-major storage, the innermost loop walks along i, so A and C
     * are accessed contiguously. This is the key architectural idea reused
     * from the Gemm_Evaluation project.
     */
    const int ld = n;

    zero_matrix(n, C);

    for (int p = 0; p < n; ++p)
    {
        for (int j = 0; j < n; ++j)
        {
            const double bpj = B[IDX(p, j, ld)];

            for (int i = 0; i < n; ++i)
            {
                C[IDX(i, j, ld)] += A[IDX(i, p, ld)] * bpj;
            }
        }
    }
}

static void gemm_blocked_outer_product(
    int n,
    const double *A,
    const double *B,
    double *C,
    int block_size)
{
    /*
     * Simple blocked outer-product GEMM.
     *
     * This is not a full production BLAS microkernel. It is intentionally
     * compact and dependency-free, but it introduces a realistic HPC idea:
     * blocking/tiling for better cache reuse.
     */
    const int ld = n;

    zero_matrix(n, C);

    for (int jj = 0; jj < n; jj += block_size)
    {
        const int j_end = (jj + block_size < n) ? jj + block_size : n;

        for (int pp = 0; pp < n; pp += block_size)
        {
            const int p_end = (pp + block_size < n) ? pp + block_size : n;

            for (int j = jj; j < j_end; ++j)
            {
                for (int p = pp; p < p_end; ++p)
                {
                    const double bpj = B[IDX(p, j, ld)];

                    for (int i = 0; i < n; ++i)
                    {
                        C[IDX(i, j, ld)] += A[IDX(i, p, ld)] * bpj;
                    }
                }
            }
        }
    }
}

static double max_abs_diff(int n, const double *X, const double *Y)
{
    const int ld = n;
    double max_diff = 0.0;

    for (int j = 0; j < n; ++j)
    {
        for (int i = 0; i < n; ++i)
        {
            const double diff = fabs(X[IDX(i, j, ld)] - Y[IDX(i, j, ld)]);

            if (diff > max_diff)
            {
                max_diff = diff;
            }
        }
    }

    return max_diff;
}

static void print_metrics(int n, const double *C)
{
    const int ld = n;

    double checksum = 0.0;
    double weighted_checksum = 0.0;
    double diagonal_sum = 0.0;
    double max_abs_value = 0.0;

    for (int j = 0; j < n; ++j)
    {
        for (int i = 0; i < n; ++i)
        {
            const double value = C[IDX(i, j, ld)];
            const double abs_value = fabs(value);

            checksum += value;
            weighted_checksum += value * (double)((i + 1) * (j + 1));

            if (i == j)
            {
                diagonal_sum += value;
            }

            if (abs_value > max_abs_value)
            {
                max_abs_value = abs_value;
            }
        }
    }

    printf("CHECKSUM %.17e\n", checksum);
    printf("WEIGHTED_CHECKSUM %.17e\n", weighted_checksum);
    printf("DIAGONAL_SUM %.17e\n", diagonal_sum);
    printf("MAX_ABS_VALUE %.17e\n", max_abs_value);
}

int main(int argc, char **argv)
{
    const int n = parse_size(argc, argv);
    const int block_size = 16;
    const size_t count = (size_t)n * (size_t)n;

    double *A = (double *)malloc(count * sizeof(double));
    double *B = (double *)malloc(count * sizeof(double));
    double *C_inner = (double *)malloc(count * sizeof(double));
    double *C_outer = (double *)malloc(count * sizeof(double));
    double *C_blocked = (double *)malloc(count * sizeof(double));

    if (A == NULL || B == NULL || C_inner == NULL || C_outer == NULL || C_blocked == NULL)
    {
        fprintf(stderr, "ERROR: memory allocation failed.\n");

        free(A);
        free(B);
        free(C_inner);
        free(C_outer);
        free(C_blocked);

        return EXIT_FAILURE;
    }

    initialize_matrices(n, A, B);

    gemm_inner_product(n, A, B, C_inner);
    gemm_outer_product(n, A, B, C_outer);
    gemm_blocked_outer_product(n, A, B, C_blocked, block_size);

    const double diff_inner_outer = max_abs_diff(n, C_inner, C_outer);
    const double diff_inner_blocked = max_abs_diff(n, C_inner, C_blocked);

    printf("KERNEL GEMM_FP64_ADVANCED_POC\n");
    printf("SIZE %d\n", n);
    printf("BLOCK_SIZE %d\n", block_size);

    /*
     * The printed validation metrics are taken from the blocked kernel because
     * it is the most architecture-aware implementation in this standalone PoC.
     */
    print_metrics(n, C_blocked);

    printf("MAX_DIFF_INNER_OUTER %.17e\n", diff_inner_outer);
    printf("MAX_DIFF_INNER_BLOCKED %.17e\n", diff_inner_blocked);

    if (diff_inner_outer <= 1.0e-10 && diff_inner_blocked <= 1.0e-10)
    {
        printf("VALIDATION_STATUS PASS\n");
    }
    else
    {
        printf("VALIDATION_STATUS FAIL\n");
    }

    free(A);
    free(B);
    free(C_inner);
    free(C_outer);
    free(C_blocked);

    return EXIT_SUCCESS;
}