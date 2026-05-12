# RISC-V FP64 Portability Proof of Concept

This directory contains a small proof of concept for testing numerical portability between native x86_64 execution and RISC-V execution through QEMU.

The goal is to keep the workflow simple, reproducible, and easy to extend later to real HPC applications from the project list.

---

## What this PoC does

The workflow performs five basic steps:

1. Compile a small FP64 GEMM-style kernel natively.
2. Run the native binary.
3. Cross-compile the same kernel for RISC-V.
4. Run the RISC-V binary with QEMU.
5. Compare the numerical outputs with a Python validator.

---

## Files

```text
hpc_validation_poc/
├── gemm_poc.c
├── portability_test.sh
├── validate_outputs.py
└── tests/
    ├── fixtures/
    └── test_validate_outputs.py
```

### `gemm_poc.c`

Small C kernel that performs double-precision GEMM-style computations.

It prints deterministic metrics such as:

```text
SIZE
BLOCK_SIZE
CHECKSUM
WEIGHTED_CHECKSUM
DIAGONAL_SUM
MAX_ABS_VALUE
MAX_DIFF_INNER_OUTER
MAX_DIFF_INNER_BLOCKED
VALIDATION_STATUS
```

These metrics are used to compare the native and RISC-V runs.

### `portability_test.sh`

Main script for the portability smoke test.

It compiles the kernel natively, runs it, cross-compiles it for RISC-V, executes the RISC-V binary through QEMU, and then calls the Python validator.

### `validate_outputs.py`

Python validator that compares the native and RISC-V outputs using a numerical tolerance.

It checks:

- validation status,
- matching metric names,
- numerical differences,
- missing metrics,
- invalid numerical values.

### `tests/`

Contains small controlled examples used to test the validator with PASS and FAIL cases.

---

## Requirements

Tested on:

```text
Ubuntu 24.04
x86_64 host
gcc
riscv64-linux-gnu-gcc
qemu-riscv64-static
python3
```

Required packages:

```bash
sudo apt install -y build-essential gcc-riscv64-linux-gnu qemu-user-static python3
```

---

## Run the portability test

From the repository root:

```bash
./hpc_validation_poc/portability_test.sh
```

Expected final message:

```text
PASS: native and RISC-V outputs match within FP64 tolerance.

================================================================
Portability smoke test completed successfully.
================================================================
```

The script creates a local `build/` directory with generated binaries and output files. This directory is ignored by Git.

---

## Run validator tests

From the repository root:

```bash
python3 hpc_validation_poc/tests/test_validate_outputs.py
```

The test script checks the validator against controlled PASS and FAIL cases.

---

## Current scope

This is an initial local smoke test. It is not a full porting framework yet.

The next step is to apply the same workflow to a small real application or benchmark from the RISC-V HPC project list.
