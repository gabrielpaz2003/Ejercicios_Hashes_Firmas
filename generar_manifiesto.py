import argparse
import hashlib
from pathlib import Path


def sha256_archivo(ruta):
    hash_sha256 = hashlib.sha256()
    with open(ruta, "rb") as archivo:
        while bloque := archivo.read(8192):
            hash_sha256.update(bloque)
    return hash_sha256.hexdigest()


def obtener_archivos():
    parser = argparse.ArgumentParser()
    parser.add_argument("archivos", nargs="+")
    args = parser.parse_args()
    return [Path(ruta) for ruta in args.archivos]


def main():
    archivos = obtener_archivos()

    if len(archivos) < 5:
        print("Debes indicar al menos 5 archivos.")
        return

    lineas = []

    for ruta in archivos:
        hash_archivo = sha256_archivo(ruta)
        lineas.append(f"{hash_archivo} {ruta.as_posix()}")

    Path("SHA256SUMS.txt").write_text("\n".join(lineas) + "\n", encoding="utf-8")

    print("SHA256SUMS.txt generado con estos archivos:")
    for linea in lineas:
        print(linea)


if __name__ == "__main__":
    main()
