#!/usr/bin/env bash
#
# portability_test.sh
#
# Local RISC-V portability smoke test.
#
# This script validates a dependency-free FP64 GEMM kernel by:
# 1. Compiling it natively on the host system.
# 2. Cross-compiling it for riscv64.
# 3. Running the RISC-V binary through qemu-riscv64-static.
# 4. Calling validate_outputs.py to compare numerical results.
#   Ubuntu 24.04 

set -euo pipefail # stop is some part fail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
POC_DIR="${ROOT_DIR}/hpc_validation_poc"
BUILD_DIR="${POC_DIR}/build"

SRC_FILE="${POC_DIR}/gemm_poc.c"
#VALIDATOR="${POC_DIR}/validate_outputs.py"
VALIDATOR="${POC_DIR}/validate_v2.py"

NATIVE_BIN="${BUILD_DIR}/gemm_native"
RISCV_BIN="${BUILD_DIR}/gemm_riscv64"

NATIVE_OUT="${BUILD_DIR}/native_output.txt"
RISCV_OUT="${BUILD_DIR}/riscv_output.txt"

NATIVE_CC="${NATIVE_CC:-gcc}"
RISCV_CC="${RISCV_CC:-riscv64-linux-gnu-gcc}"
QEMU_RISCV="${QEMU_RISCV:-qemu-riscv64-static}"

ABS_TOL="${ABS_TOL:-1e-10}"
REL_TOL="${REL_TOL:-1e-10}"

print_header() {
    echo "================================================================"
    echo "        RISC-V HPC Portability Smoke Test - FP64 GEMM            "
    echo "================================================================"
    echo "Host system      : $(uname -s)/$(uname -m)"
    echo "Source file      : ${SRC_FILE}"
    echo "Validator        : ${VALIDATOR}"
    echo "Build directory  : ${BUILD_DIR}"
    echo "Native compiler  : ${NATIVE_CC}"
    echo "RISC-V compiler  : ${RISCV_CC}"
    echo "RISC-V emulator  : ${QEMU_RISCV}"
    echo "Abs tolerance    : ${ABS_TOL}"
    echo "Rel tolerance    : ${REL_TOL}"
    echo "----------------------------------------------------------------"
}

require_command() {
    local cmd="$1"

    if ! command -v "${cmd}" >/dev/null 2>&1; then
        echo "[ERROR] Required command not found: ${cmd}"
        echo
        echo "Install dependencies on Ubuntu 24.04 with:"
        echo "  sudo apt install -y build-essential gcc-riscv64-linux-gnu qemu-user-static python3"
        exit 1
    fi
}

check_dependencies() {
    require_command "${NATIVE_CC}"
    require_command "${RISCV_CC}"
    require_command "${QEMU_RISCV}"
    require_command "python3"

    if [[ ! -f "${SRC_FILE}" ]]; then
        echo "[ERROR] Source file not found: ${SRC_FILE}"
        exit 1
    fi

    if [[ ! -f "${VALIDATOR}" ]]; then
        echo "[ERROR] Validator not found: ${VALIDATOR}"
        exit 1
    fi
}

build_native() {
    echo "[1/5] Compiling native host binary..."

    "${NATIVE_CC}" \
        -O2 \
        -std=c11 \
        -Wall \
        -Wextra \
        -pedantic \
        -ffp-contract=off \
        "${SRC_FILE}" \
        -lm \
        -o "${NATIVE_BIN}"
}

run_native() {
    echo "[2/5] Running native binary..."
    "${NATIVE_BIN}" > "${NATIVE_OUT}"
}

build_riscv() {
    echo "[3/5] Cross-compiling riscv64 binary..."

    "${RISCV_CC}" \
        -O2 \
        -std=c11 \
        -Wall \
        -Wextra \
        -pedantic \
        -ffp-contract=off \
        -static \
        -march=rv64gc \
        -mabi=lp64d \
        "${SRC_FILE}" \
        -lm \
        -o "${RISCV_BIN}"
}

run_riscv() {
    echo "[4/5] Running riscv64 binary with QEMU..."
    "${QEMU_RISCV}" "${RISCV_BIN}" > "${RISCV_OUT}"
}

validate_outputs() {
    echo "[5/5] Validating numerical output..."

    python3 "${VALIDATOR}" \
        --native-output "${NATIVE_OUT}" \
        --riscv-output "${RISCV_OUT}" \
        --atol "${ABS_TOL}"
        #--rel-tol "${REL_TOL}"
}

main() {
    mkdir -p "${BUILD_DIR}"

    print_header
    check_dependencies
    build_native
    run_native
    build_riscv
    run_riscv
    validate_outputs

    echo
    echo "Native output:"
    cat "${NATIVE_OUT}"

    echo
    echo
    echo "RISC-V output:"
    cat "${RISCV_OUT}"

    echo
    echo
    echo "================================================================"
    echo "Portability smoke test completed successfully."
    echo "================================================================"
}

main "$@"