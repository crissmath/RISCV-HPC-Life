# LFX Mentorship Summer 2026: RISC-V HPC Portability & Optimization

**Applicant:** crissmath  
**Target Project:** Broadening the RISC-V High Precision Code Base and Reach  
**Mentor:** Kurt Keville, MIT  

---

## 1. Coding Challenge

This section contains the coding challenge requested for the project application.

The challenge asks for a short scripted demonstration of either **Tower of Hanoi** or **Conway's Game of Life**, ideally identifying the sections that demonstrate recursion and/or iteration.

This repository currently provides a working **Tower of Hanoi** implementation in **Bash**.

### Current Challenge Coverage

- **Tower of Hanoi (Bash):** implemented and fully runnable.
- **Main concept demonstrated:** recursion.
- **Execution style:** command-line script with formatted terminal output.
- **Optional extension:** Conway's Game of Life notes are included for future iterative simulation work.

---

## 2. Tower of Hanoi Implementation

**File:** `hanoi_tower.sh`

The Tower of Hanoi algorithm is implemented recursively.

The core recursive structure is:

```bash
hanoi_solve "$((n - 1))" "$source" "$target" "$aux"
move_disk "$n" "$source" "$target"
hanoi_solve "$((n - 1))" "$aux" "$source" "$target"
```

The recursion follows the classical three-step strategy:

1. Move `n - 1` disks from the source peg to the auxiliary peg.
2. Move the largest disk from the source peg to the target peg.
3. Move the `n - 1` disks from the auxiliary peg to the target peg.

This demonstrates recursive decomposition, base-case handling, and repeated function calls in a Bash script.

---

## 3. How to Run the Coding Challenge

Make the script executable:

```bash
chmod +x hanoi_tower.sh
```

Run with the default number of disks:

```bash
./hanoi_tower.sh
```

Run with a custom number of disks:

```bash
./hanoi_tower.sh 10
```

Example output:

```text
================================================================
                   TOWER OF HANOI                               
================================================================
Config: 3 disks      |      System: Linux/x86_64
----------------------------------------------------------------
[Step 01] (Disk 1): P_A --> P_C
[Step 02] (Disk 2): P_A --> P_B
[Step 03] (Disk 1): P_C --> P_B
[Step 04] (Disk 3): P_A --> P_C
[Step 05] (Disk 1): P_B --> P_A
[Step 06] (Disk 2): P_B --> P_C
[Step 07] (Disk 1): P_A --> P_C
--------------------------------------------------------------
 Simulation completed in 7 steps.
--------------------------------------------------------------
================================================================
```

---

## 4. RISC-V HPC Portability Proof of Concept

**Directory:** `hpc_validation_poc/`

The target mentorship project focuses on refactoring, compiling, validating, and optimizing community AI/ML and HPC applications for RISC-V.

To demonstrate readiness for that type of work, this repository also includes an initial local proof of concept focused on:

- Native compilation on the host architecture.
- RISC-V cross-compilation.
- RISC-V execution through QEMU.
- Double-precision numerical validation.
- Early automation patterns for scaling portability checks.

This proof of concept is intentionally small, but it models the kind of workflow required to test scientific and engineering codes across architectures.

---

## 5. Double-Precision Validation Kernel

**Current file:** `hpc_validation_poc/gemm_advanced.c`

The validation kernel uses double-precision floating-point operations to simulate a small HPC-style numerical workload.

The intended validation flow is:

1. Compile the numerical kernel natively on the host system.
2. Cross-compile the same source code for RISC-V.
3. Execute the RISC-V binary using QEMU.
4. Compare the native and RISC-V outputs.
5. Detect numerical deviations using tolerance-based validation.

This is relevant because many HPC applications depend on numerical stability, reproducibility, and double-precision correctness.

---

## 6. Planned Portability Automation

The next step is to add a local portability script:

```text
hpc_validation_poc/portability_test.sh
```

The script will automate the following workflow:

```text
native compile -> native run -> RISC-V cross-compile -> QEMU run -> output validation
```

This provides a small but extensible base that can later be adapted to test larger applications from the RISC-V HPC code list.

---

## 7. Relevance to the 400-Code Porting Effort

Refactoring and compiling a large set of HPC and AI/ML applications requires more than manual compilation. It requires a repeatable process for:

- Classifying codes by language, build system, and dependencies.
- Detecting portability issues early.
- Checking RISC-V package availability.
- Cross-compiling where possible.
- Running smoke tests under emulation.
- Validating numerical behavior for double-precision workloads.

The proof of concept in this repository is a small first step toward that kind of automated workflow.

---

## 8. Proposed Optimization Strategy

The broader strategy for the mentorship project can be organized into four phases:

### Phase 1: Codebase Triage

Classify target applications by:

- Programming language.
- Build system.
- Dependency stack.
- Numerical workload type.
- Current package availability.
- Expected RISC-V portability difficulty.

### Phase 2: Automated Build and Portability Testing

Develop repeatable scripts for:

- Native builds.
- RISC-V cross-compilation.
- QEMU-based smoke testing.
- Build log collection.
- Failure classification.

### Phase 3: Numerical Validation

Compare native and RISC-V results using:

- Deterministic test cases.
- Double-precision kernels.
- Tolerance-based output checks.
- Reproducible validation logs.

### Phase 4: Architecture-Aware Optimization

Identify and address performance bottlenecks related to:

- Memory access patterns.
- Cache behavior.
- Vectorization opportunities.
- Architecture-specific assumptions.
- Future use of the RISC-V Vector Extension where appropriate.

---

## 9. Repository Layout

Current layout:

```text
RISCV-HPC-Life/
├── README.md
├── hanoi_tower.sh
├── Con_game_notes.md
└── hpc_validation_poc/
    ├── gemm_advanced.c
    └── src/
```

Planned additions:

```text
hpc_validation_poc/
├── README.md
├── PORTING_METHODOLOGY.md
├── portability_test.sh
└── gemm_poc.c
```

---

## 10. Development Environment

Current development environment:

```text
Host OS: Ubuntu 24.04
Primary scripting language: Bash
Optional scripting language: Python
Target architecture: riscv64
Emulation target: QEMU riscv64
Toolchain target: riscv64-linux-gnu-gcc
```

Usefull: compiler flags

**x86**
gcc -O2 -std=c11 -Wall -Wextra -pedantic -ffp-contract=off hpc_validation_poc/gemm_poc.c -lm -o hpc_validation_poc/gemm_native_test

```bash
gcc                         compilador C nativo
-O2                         optimización razonable
-std=c11                    usar estándar C11
-Wall                       advertencias comunes
-Wextra                     advertencias adicionales
-pedantic                   advertir sobre extensiones no estándar
-ffp-contract=off           evitar FMA automático para comparación FP más estable
hpc_validation_poc/gemm_poc.c   archivo fuente
-lm                         enlazar biblioteca matemática
-o gemm_native_test         nombre del ejecutable final
```

```bash
$ ./gemm_native_test 
KERNEL GEMM_FP64_ADVANCED_POC
SIZE 64
BLOCK_SIZE 16
CHECKSUM 6.12822580645161494e+01
WEIGHTED_CHECKSUM 5.48819899888765067e+04
DIAGONAL_SUM -2.05297552836485186e+00
MAX_ABS_VALUE 4.21913236929922242e+00
MAX_DIFF_INNER_OUTER 0.00000000000000000e+00
MAX_DIFF_INNER_BLOCKED 0.00000000000000000e+00
VALIDATION_STATUS PASS
```

**risc-v**
riscv64-linux-gnu-gcc -O2 -std=c11 -Wall -Wextra -pedantic -ffp-contract=off -static -march=rv64gc -mabi=lp64d hpc_validation_poc/gemm_poc.c -lm -o hpc_validation_poc/gemm_riscv64_test

```bash
:~/RISCV-HPC-Life/hpc_validation_poc$ qemu-riscv64-static gemm_riscv64_test 
KERNEL GEMM_FP64_ADVANCED_POC
SIZE 64
BLOCK_SIZE 16
CHECKSUM 6.12822580645161494e+01
WEIGHTED_CHECKSUM 5.48819899888765067e+04
DIAGONAL_SUM -2.05297552836485186e+00
MAX_ABS_VALUE 4.21913236929922242e+00
MAX_DIFF_INNER_OUTER 0.00000000000000000e+00
MAX_DIFF_INNER_BLOCKED 0.00000000000000000e+00
VALIDATION_STATUS PASS
```

---

## 11. Summary

This repository satisfies the coding challenge through a working Bash implementation of the Tower of Hanoi algorithm.

It also extends the submission with an initial RISC-V HPC portability proof of concept focused on double-precision validation, cross-compilation, QEMU-based execution, and automation patterns relevant to the broader 400-code porting effort.

The goal is to demonstrate not only scripting ability, but also readiness to contribute to automated portability, validation, and optimization workflows for high-precision scientific applications on RISC-V.

---

*Ready to contribute to the RISC-V HPC software ecosystem.*
