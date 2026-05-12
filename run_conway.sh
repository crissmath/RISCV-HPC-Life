#!/usr/bin/env bash
set -euo pipefail

PATTERN_FILE="${1:-}"
GENERATIONS="${2:-10}"

if [[ "${PATTERN_FILE}" == "" ]]; then
    echo "Usage"
    echo " ./run_conway.sh pattern_file.txt"
    echo "./run_conway.sh pattern_file.txt generations"
    exit 1
fi

if [[ ! -f "${PATTERN_FILE}" ]]; then
    echo "Error: pattern file not found: ${PATTERN_FILE}"
    exit 1
fi 

python3 conway_life.py "${PATTERN_FILE}" "${GENERATIONS}"