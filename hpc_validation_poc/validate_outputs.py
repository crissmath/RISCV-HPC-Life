import sys


def validate():
    print("--- Auditoría de Precisión Numérica (FP64) ---")

    try:
        with open("build/out_x86.txt", "r") as f_x86, open(
            "build/out_riscv.txt", "r"
        ) as f_rv:

            x86_data = f_x86.readlines()
            rv_data = f_rv.readlines()

        if len(x86_data) != len(rv_data):
            print("FALLO: El número de líneas no coincide.")
            return False

        # Double Precision
        # 1e-9 normal standar GEMM base
        atol = 1e-9

        passed = True
        for i, (line_x, line_r) in enumerate(zip(x86_data, rv_data)):
            val_x = [float(x) for x in line_x.split()]
            val_r = [float(r) for r in line_r.split()]

            for j, (v_x, v_r) in enumerate(zip(val_x, val_r)):
                if abs(v_x - v_r) > atol:
                    print(f"ERROR en línea {i+1}, columna {j+1}:")
                    print(f"   x86: {v_x} | RISC-V: {v_r} | Delta: {abs(v_x - v_r)}")
                    passed = False

        if passed:
            print(
                "PASS: Los resultados de x86 y RISC-V son idénticos dentro del margen de error."
            )
            return True
        else:
            return False

    except FileNotFoundError:
        print("ERROR: No se encontraron los archivos de salida en la carpeta 'build/'.")
        return False
    except Exception as e:
        print(f"ERROR inesperado: {e}")
        return False


if __name__ == "__main__":
    if not validate():
        sys.exit(1)
