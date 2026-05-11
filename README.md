cat << 'EOF' > README.md

# LFX Mentorship Summer 2026: RISC-V HPC Portability & Optimization

**Applicant:** crissmath  
**Target Project:** Broadening the RISC-V High Precision Code Base and Reach (Mentor: Kurt Keville, MIT)

---

## 1. The Coding Challenge

This section contains the solutions requested for the project application. It includes a simple **Tower of Hanoi** demonstration implemented in **Bash**, and is currently being extended with a **Conway's Game of Life** implementation in **Python**.

### Current Challenge Coverage

- **Tower of Hanoi (Bash)**: Demonstrates a recursive solution with formatted terminal output.
- **Conway's Game of Life (Python)**: Planned as an additional dynamic example for the challenge.

### Tower of Hanoi Implementation

The Tower of Hanoi is implemented recursively using two core calls:

```bash
hanoi_solve "$((n - 1))" "$source" "$target" "$aux"
hanoi_solve "$((n - 1))" "$aux" "$source" "$target"
```

### How to Run
The script uses 3 disks by default. To increase the complexity, pass the desired number of disks as a parameter (e.g., `./hanoi_tower.sh 10`).

**Default run:**
```bash
./hanoi_tower.sh
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

### Conway's Game of Life
To be continued ... :P

---

## 2. HPC Porting & Double Precision Validation (The PoC)

**Directory:** `hpc_validation_poc/`

Refactoring and compiling ~400 HPC and AI/ML applications is a task that demands deep automation and strict numerical compliance. To demonstrate readiness for this core challenge, I have built a foundational CI/CD pipeline tailored for High-Performance Computing.

### The Proof of Concept:
I implemented a Double-Precision General Matrix Multiplication (GEMM) kernel (`gemm_poc.c`) to simulate the computational workload of the target applications. The provided script (`portability_test.sh`) automates the following pipeline:
1.  **Native Compilation:** Compiles the C code for the host architecture (x86) to establish a mathematical baseline.
2.  **Cross-Compilation:** Uses `riscv64-linux-gnu-gcc` to generate the RISC-V binary.
3.  **Emulation:** Executes the RISC-V binary using `qemu-riscv64-static`.
4.  **Strict Validation:** Automatically diffs the output between x86 and RISC-V to guarantee zero loss of floating-point precision (Double Precision accuracy).

### Why this matters for the 400 codes:
This script represents the core engine of the automation we will build this summer. Instead of manually porting codes, this pipeline will be scaled to batch-ingest the 400 targets, handle dependencies, and automatically flag precision anomalies across the entire spreadsheet.

---

## 3. Optimization Strategy

Please refer to [`hpc_validation_poc/PORTING_METHODOLOGY.md`](hpc_validation_poc/PORTING_METHODOLOGY.md) for my detailed, 4-phase architectural plan on how we will tackle the codebase. The methodology covers:
*   Automated cross-compilation at scale.
*   Strict numerical validation against *Numerical Recipes* tolerances.
*   Hardware Abstraction Layer (HAL) design for transitioning legacy x86 intrinsics to **RISC-V Vector Extension (RVV)**.
*   Silicon-level profiling for memory bandwidth and cache optimization.

---
*Ready to contribute to the HAL-T repository and accelerate the RISC-V ecosystem.*
EOF
