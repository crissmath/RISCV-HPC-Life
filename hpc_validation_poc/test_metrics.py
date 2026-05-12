from validate_v2 import read_metrics, validate

metrics, estado = read_metrics("test_output.txt")


# print(f"typo de Numeric_keys {NUMERIC_KEYS}")

print("========================")
print(f"   ESTADO", {estado})
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
valid = validate("native_.txt", "riscv_output.txt", 1e-9)
