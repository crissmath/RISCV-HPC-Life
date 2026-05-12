# RISCV-HPC-Life

## 1. Coding Challenge

This repository was created for the coding challenge of the LFX Mentorship project:

**Broadening the RISC-V High Precision Code Base and Reach**

The requested task was to create a short scripted demonstration of either:

- Tower of Hanoi
- Conway's Game of Life

The current implementation provides a working **Tower of Hanoi** demonstration written in **Bash**, and Conway's Game of Life demo in Python

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

### Rules

```text
live cell + fewer than 2 live neighbors  -> dead cell
live cell + 2 or 3 live neighbors        -> live cell
live cell + more than 3 live neighbors   -> dead cell
dead cell + exactly 3 live neighbors     -> live cell
dead cell + any other number of neighbors -> dead cell
```

### Run the basic demo

```bash
python3 conway_life.py
```

Example output:

```text
Generation 0
......
..X...
..X...
..X...
......

Generation 1
......
......
.XXX..
......
......

*
*
*

Generation 5
......
......
.XXX..
......
......

```

### Run external patters from file

```bash
./run_conway.sh pattern_file.txt 5
```

```text
param 1: file with commont patterns
param 2: number of generations 
```

Example output:

```bash
./run_conway.sh pattern_file.txt 5
Generation 0
..............................
..............................
..XX.................XX.......
..XX................X..X......
.....................XX.......
..............................
..............................
..............................
..............................
.....X........................
.....X.........XXX............
.....X........XXX.............
..............................
..............................
........................X.....
.........................X....
.......................XXX....
..............................
..............................
..............................

Generation 1
..............................
..............................
..XX.................XX.......
..XX................X..X......
.....................XX.......
..............................
..............................
..............................
..............................
................X.............
....XXX.......X..X............
..............X..X............
...............X..............
..............................
..............................
.......................X.X....
........................XX....
........................X.....
..............................
..............................

*
*
*

Generation 5
..............................
..............................
..XX.................XX.......
..XX................X..X......
.....................XX.......
..............................
..............................
..............................
..............................
................X.............
....XXX.......X..X............
..............X..X............
...............X..............
..............................
..............................
..............................
........................X.X...
.........................XX...
.........................X....
..............................
```

## 4. RISC-V FP64 Portability Proof of Concept

After completing the required scripting challenge, I added a small local proof of concept related to the broader mentorship project.

The project focuses on refactoring, compiling, validating, and optimizing AI/ML and HPC applications for RISC-V, especially double-precision workloads.

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
step 1: native compile
step 2: native run
step 3: RISC-V cross-compile
step 4: RISC-V run through QEMU
step 5: FP64 numerical validation
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
├── hanoi_tower.sh
├── conway_life.py
├── run_conway.sh
├── pattern_file.txt
└── hpc_validation_poc/
    ├── README.md
    ├── gemm_poc.c
    ├── portability_test.sh
    ├── validate_outputs.py
    └── tests/                  # Local test files for validating the helper functions
```

---
