# RISCV-HPC-Life

Coding Challenge - Broadening the RISC-V High Precision Code Base and Reach

This repository imclud a simple **Tower of Hanoi** demonstration implemented in **BASH**.
It is also being extended with a **Conway's Game of the life** implementation in **Python**.

## Current challenge coverage

- **Tower of Hanoi (BASH)**: Desmostrate recursive solition with terminal output.
- **Conway's Game of life(Python)**: planned as an additional example for the challenge.

## Tower of Hanoi

The tower of Hanoi is implemented recursively.

recursive using two calls:

```bash
hanoi_solve "$(n - 1)" "$source" "$target" "$aux"
hanoi_solve "$(n - 1)" "$aux" "$source" "$target"
```

## How to run

For default use 3 disks, but if you want to increment use parameter (./hanoi_tower.sh 10)

custom run:

```bash
./hanoi_tower.sh 10
```

defaul run:

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

## **Conway's Game of life**

To be continued ... :P
