# RISCV-HPC-Life

Coding Challenge - Broadening the RISC-V High Precision Code Base and Reach

This repository contains a simple **Tower of Hanoi** demonstration implemented in BASH and Conway's Game of Life in Python.

## What it shows

- A correct recursive solution to the Tower of Hanoi problem
- Clear separation of the recursive steps
- Simple terminal-based output to demonstrate functionality

## Recursion

The recursive structure appears in these two calls:

```bash
hanoi_solve (n - 1) origin destination, auxiliary
hanoi_solve (n - 1) auxiliary origin destination
