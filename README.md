# LFX Mentorship Summer 2026: RISC-V HPC Portability & Optimization

**Applicant:** crissmath  
**Target Project:** Broadening the RISC-V High Precision Code Base and Reach  
**Focus:** scripting challenge, RISC-V portability, FP64 validation, and early automation for HPC codes

---

## 1. Coding Challenge

This repository was created for the coding challenge of the LFX Mentorship project:

**Broadening the RISC-V High Precision Code Base and Reach**

The requested task was to create a short scripted demonstration of either:

- Tower of Hanoi
- Conway's Game of Life

The current implementation provides a working **Tower of Hanoi** demonstration written in **Bash**.

---

## 2. Tower of Hanoi Demo

**File:** `hanoi_tower.sh`

The Tower of Hanoi implementation demonstrates recursion in a simple command-line script.

The recursive structure is based on the classical three-step decomposition:

1. Move `n - 1` disks from the source peg to the auxiliary peg.
2. Move the largest disk from the source peg to the target peg.
3. Move the `n - 1` disks from the auxiliary peg to the target peg.

The core recursive calls are:

```bash
hanoi_solve "$((n - 1))" "$source" "$target" "$aux"
move_disk "$n" "$source" "$target"
hanoi_solve "$((n - 1))" "$aux" "$source" "$target"
```

### Run the challenge demo

```bash
chmod +x hanoi_tower.sh
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

## 3. Conway's Game of Life Demo

**File:** `conway_life.py`

Conway's Game of Life is included as a small Python demonstration of iteration.

The script starts from a fixed board, counts the live neighbors of each cell, applies Conway's rules, and generates the next board state. Repeating this process shows how the board evolves generation by generation.

### Rules

```text
live cell + fewer than 2 live neighbors  -> dead cell
live cell + 2 or 3 live neighbors        -> live cell
live cell + more than 3 live neighbors   -> dead cell
dead cell + exactly 3 live neighbors     -> live cell
dead cell + any other number of neighbors -> dead cell
```

### Run the demo

```python
python3 conway_life.py
```

## 4. RISC-V FP64 Portability Proof of Concept

After completing the required scripting challenge, I added a small local proof of concept related to the broader mentorship project.

The project description focuses on refactoring, compiling, validating, and optimizing AI/ML and HPC applications for RISC-V, especially high-precision double-precision workloads.

To explore that direction, this repository includes a small FP64 GEMM-style validation workflow.

**Directory:** `hpc_validation_poc/`

The proof of concept currently performs:

1. Native compilation on the host system.
2. RISC-V cross-compilation using `riscv64-linux-gnu-gcc`.
3. RISC-V execution using `qemu-riscv64-static`.
4. Numerical validation between native and RISC-V outputs.
5. Small validator tests using controlled PASS and FAIL fixtures.

This is intentionally small, but it models the kind of workflow needed before scaling to larger HPC applications.

---

## 5. FP64 GEMM Kernel

**File:** `hpc_validation_poc/gemm_poc.c`

The numerical kernel is a dependency-free C implementation inspired by GEMM evaluation work.

It includes:

- Inner-product GEMM baseline.
- Outer-product GEMM formulation.
- Blocked outer-product GEMM variant.
- Deterministic FP64 metrics for validation.

The program prints metrics such as:

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

These metrics are used to compare native execution against RISC-V execution under QEMU.

---

## 6. Portability Test Script

**File:** `hpc_validation_poc/portability_test.sh`

The script automates the local portability workflow:

```text
native compile
      ↓
native run
      ↓
RISC-V cross-compile
      ↓
RISC-V run through QEMU
      ↓
FP64 numerical validation
```

Run it with:

```bash
./hpc_validation_poc/portability_test.sh
```

Expected final result:

```text
PASS: native and RISC-V outputs match within FP64 tolerance.

================================================================
Portability smoke test completed successfully.
================================================================
```

---

## 7. Numerical Validator

**File:** `hpc_validation_poc/validate_outputs.py`

The validator reads the output generated by the native and RISC-V binaries, extracts numerical metrics, and compares them using an FP64 tolerance.

It currently checks:

- Matching validation status.
- Matching metric sets.
- Numerical differences within tolerance.
- Missing metrics.
- Invalid numerical values.

Validator tests are included under:

```text
hpc_validation_poc/tests/
```

Run the validator tests with:

```bash
python3 hpc_validation_poc/tests/test_validate_outputs.py
```

---

## 8. Repository Layout

```text
RISCV-HPC-Life/
├── README.md
├── conway_life.py
├── hanoi_tower.sh
└── hpc_validation_poc
    ├── README.md
    ├── gemm_poc.c
    ├── portability_test.sh
    ├── tests
    │   ├── fixtures
    │   │   ├── native_output_pass.txt
    │   │   ├── riscv_output_bad_number.txt
    │   │   ├── riscv_output_fail_delta.txt
    │   │   ├── riscv_output_fail_status.txt
    │   │   ├── riscv_output_missing_metric.txt
    │   │   └── riscv_output_pass.txt
    │   └── test_validate_outputs.py
    └── validate_outputs.py
```

The `build/` directory is generated locally by the portability script and is intentionally ignored by Git.

---

## 9. Development Environment

Current local test environment:

```text
Host OS: Ubuntu 24.04 / WSL2
Host architecture: x86_64
Native compiler: gcc
RISC-V compiler: riscv64-linux-gnu-gcc
RISC-V emulator: qemu-riscv64-static
Validation language: Python 3
```

---

## 10. Current Status

Completed:

- Tower of Hanoi Bash challenge.
- Conway's Game of Life Python iteration demo
- Local FP64 GEMM portability kernel.
- Native compilation and execution.
- RISC-V cross-compilation.
- RISC-V execution through QEMU.
- Tolerance-based numerical validation.
- Controlled validator test cases.

Planned next step:

- Apply the same workflow to a small real application or benchmark from the project list.

---

## 10. Summary

This repository satisfies the required coding challenge with a Bash implementation of Tower of Hanoi.

It also includes a small RISC-V FP64 portability proof of concept that demonstrates the first steps toward automated validation for high-precision HPC workloads.

The goal is to keep the implementation simple, reproducible, and extensible before scaling the workflow to real applications from the project list.
