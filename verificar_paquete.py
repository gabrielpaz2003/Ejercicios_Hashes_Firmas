import hashlib
from pathlib import Path


def sha256_archivo(ruta):
    hash_sha256 = hashlib.sha256()
    with open(ruta, "rb") as archivo:
        while bloque := archivo.read(8192):
            hash_sha256.update(bloque)
    return hash_sha256.hexdigest()


def leer_manifiesto():
    lineas = Path("SHA256SUMS.txt").read_text(encoding="utf-8").splitlines()
    return [linea.split(maxsplit=1) for linea in lineas]


def main():
    entradas = leer_manifiesto()
    correctos = 0
    alterados = 0

    for hash_esperado, nombre_archivo in entradas:
        hash_actual = sha256_archivo(nombre_archivo)

        if hash_actual == hash_esperado:
            print(f"OK        {nombre_archivo}")
            correctos += 1
        else:
            print(f"ALTERADO  {nombre_archivo}")
            alterados += 1

    print()
    print(f"Archivos correctos: {correctos}")
    print(f"Archivos alterados: {alterados}")


if __name__ == "__main__":
    main()
