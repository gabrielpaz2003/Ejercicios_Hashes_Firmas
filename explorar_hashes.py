import hashlib


TEXTOS = ["MediSoft-v2.1.0", "medisoft-v2.1.0"]
ALGORITMOS = [
    ("MD5", hashlib.md5, 128),
    ("SHA-1", hashlib.sha1, 160),
    ("SHA-256", hashlib.sha256, 256),
    ("SHA3-256", hashlib.sha3_256, 256),
]


def calcular_hash(texto, funcion_hash):
    return funcion_hash(texto.encode("utf-8")).hexdigest()


def contar_bits_distintos(hash_a, hash_b):
    numero_a = int(hash_a, 16)
    numero_b = int(hash_b, 16)
    return (numero_a ^ numero_b).bit_count()


def main():
    print(f"{'Entrada':20} {'Algoritmo':10} {'Bits':5} {'Hex':5} Hash")
    print("-" * 110)

    sha256_hashes = []

    for texto in TEXTOS:
        for nombre, funcion_hash, bits in ALGORITMOS:
            valor = calcular_hash(texto, funcion_hash)
            print(f"{texto:20} {nombre:10} {bits:<5} {len(valor):<5} {valor}")
            if nombre == "SHA-256":
                sha256_hashes.append(valor)

    bits_distintos = contar_bits_distintos(sha256_hashes[0], sha256_hashes[1])

    print()
    print(f"Bits distintos entre ambos SHA-256: {bits_distintos}")
    print("Propiedad demostrada: efecto avalancha.")
    print("MD5 ya no es adecuado para integridad porque solo produce 128 bits y tiene colisiones conocidas.")


if __name__ == "__main__":
    main()
