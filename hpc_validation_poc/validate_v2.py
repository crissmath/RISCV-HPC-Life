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
    metrics = {}
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
            # print(f"\n[DEBUG] type:{type(NUMERIC_KEYS)}")

            if key in NUMERIC_KEYS:
                # print(f"\n[DEBUG] In to key {key}")
                metrics[key] = float(value)

    return metrics, status
