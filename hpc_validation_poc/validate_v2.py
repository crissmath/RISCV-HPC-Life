import argparse
import sys

NUMERIC_KEYS = {
    "SIZE",
    "BLOCK_SIZE",
    "CHECKSUM",
    "WEIGHTED_CHECKSUM",
    "DIAGONAL_SUM",
    "MAX_ABS_VALUE",
    "MAX_DIFF_INNER_OUTER",
    "MAX_DIFF_INNER_BLOCKED",
}


def read_metrics(path):
    metrics = {}  # dictionary
    status = None

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split()

            if len(parts) != 2:
                continue

            key, value = parts

            if key == "VALIDATION_STATUS":
                status = value
                continue

            # -- DEBUG --#
            # print(f"\n[DEBUG] llave:{key}")
            # print(f"\n[DEBUG] type:{type(key)}")
            print(f"\n[DEBUG] type:{type(NUMERIC_KEYS)}")

            if key in NUMERIC_KEYS:
                # print(f"\n[DEBUG] In to key {key}")
                metrics[key] = float(value)

    return metrics, status


def validate(native_output, riscv_output, atol):
    print(f"FP64 Numerical Validation")

    try:
        native_metrics, native_status = read_metrics(native_output)
        riscv_metrics, riscv_status = read_metrics(riscv_output)

        # check if correct
        if native_status != "PASS":
            print(f"FAIL: native validation status is {native_status}")
            return False

        if riscv_status != "PASS":
            print(f"FAIL: native validation status is {riscv_status}")
            return False

        if native_metrics.keys() != riscv_metrics.key():
            printf("FAIL:  metric sets do not match.")
            print(f"Native metrics: {sorted(native_metrics.keys())}")
            print(f"RISC-V metrics: {sorted(native_metrics.keys())}")
            return False

        passed = True  # bool for control mistake in metrics

    except FileNotFoundError as error:
        print(f"ERROR: output file not found: {error.filename}")
        return False
