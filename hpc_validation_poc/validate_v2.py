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
            # print(f"\n[DEBUG] type:{type(NUMERIC_KEYS)}")

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
            print(f"FAIL: riscv validation status is {riscv_status}")
            return False

        if native_metrics.keys() != riscv_metrics.keys():
            print("FAIL:  metric sets do not match.")
            print(f"Native metrics: {sorted(native_metrics.keys())}")
            print(f"RISC-V metrics: {sorted(riscv_metrics.keys())}")
            return False

        passed = True  # bool for control mistake in metrics

        for key in sorted(native_metrics.keys()):
            native_value = native_metrics[key]
            riscv_value = riscv_metrics[key]
            delta = abs(native_value - riscv_value)

            print(
                f"{key}:"
                f"native={native_value:.17e} |"
                f"riscv={riscv_value:.17e} |"
                f"delta={delta:.3e}"
            )

            if delta > atol:
                print(f"ERROR in metric {key}:")
                print(f"    native : {native_value}")
                print(f"    RISC-V : {riscv_value}")
                print(f"    delta : {delta}")
                passed = False

        if passed:
            print("PASS: native and RISC-V outputs match within FP64 tolerance.")
            return True

        return False

    except FileNotFoundError as error:
        print(f"ERROR: output file not found: {error.filename}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Validate native and RISC-V FP64 numerical outputs."
    )

    parser.add_argument("--native-output", required=True)
    parser.add_argument("--riscv-output", required=True)
    parser.add_argument("--atol", type=float, default=1e-9)

    arg = parser.parse_args()

    if not validate(args.native_output, args.riscv_output, args.atol):
        sys.exit(1)


if __name__ == "__main__":
    main()
