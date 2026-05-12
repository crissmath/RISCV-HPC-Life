import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
POC_DIR = CURRENT_DIR.parent
FIXTURES_DIR = CURRENT_DIR / "fixtures"

sys.path.insert(0, str(POC_DIR))


from validate_outputs import read_metrics, validate


def fixture_path(filename):
    return str(FIXTURES_DIR / filename)


metrics, estado = read_metrics(fixture_path("native_output_pass.txt"))


print("========================")
print(f"   ESTADO: {estado}")
print("========================\n")

print("captured metrics:")
if not metrics:
    print("No capture !! dict is empty")
else:
    for key, value in metrics.items():
        print(f" -> {key}: {value}")


print("========================\n")
print("     VALIDATE            ")
print("========================\n")

# 1e-9 standar for float aplications
print("\n[CASE 1] Expected PASS")
valid = validate("native_output.txt", "riscv_output.txt", 1e-9)
print(f"Result: {valid}")


print("\n[CASE 2] Expected FAIL: numerical delta")
valid = validate("native_output.txt", "riscv_output_fail_delta.txt", 1e-12)
print(f"Result: {valid}")


print("\n[CASE 3] Expected FAIL: RISC-V internal status")
valid = validate("native_output.txt", "riscv_output_fail_status.txt", 1e-9)
print(f"Result: {valid}")


print("\n[CASE 4] Expected FAIL: missing metric")
valid = validate("native_output.txt", "riscv_output_missing_metric.txt", 1e-9)
print(f"Result: {valid}")


print("\n[CASE 5] Expected FAIL: bad numerical value")
valid = validate("native_output.txt", "riscv_output_bad_number.txt", 1e-9)
print(f"Result: {valid}")
