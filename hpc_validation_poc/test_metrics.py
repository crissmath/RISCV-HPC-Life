from validate_v2 import read_metrics, validate

metrics, estado = read_metrics("test_output.txt")


# print(f"typo de Numeric_keys {NUMERIC_KEYS}")

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
