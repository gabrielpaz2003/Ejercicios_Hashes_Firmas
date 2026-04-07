import hashlib
from urllib.request import Request, urlopen


CONTRASENAS = ["admin", "123456", "hospital", "medisoft2024"]


def sha256_texto(texto):
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def sha1_texto(texto):
    return hashlib.sha1(texto.encode("utf-8")).hexdigest().upper()


def consultar_hibp(contrasena):
    hash_sha1 = sha1_texto(contrasena)
    prefijo = hash_sha1[:5]
    sufijo = hash_sha1[5:]

    request = Request(
        f"https://api.pwnedpasswords.com/range/{prefijo}",
        headers={"User-Agent": "EjercicioHashesFirmas"},
    )

    respuesta = urlopen(request).read().decode("utf-8")

    for linea in respuesta.splitlines():
        hash_sufijo, conteo = linea.split(":")
        if hash_sufijo == sufijo:
            return int(conteo)

    return 0


def main():
    for contrasena in CONTRASENAS:
        hash_sha256 = sha256_texto(contrasena)
        apariciones = consultar_hibp(contrasena)

        print(f"Contrasena: {contrasena}")
        print(f"SHA-256: {hash_sha256}")
        print(f"Apariciones en HIBP: {apariciones}")
        print()


if __name__ == "__main__":
    main()
