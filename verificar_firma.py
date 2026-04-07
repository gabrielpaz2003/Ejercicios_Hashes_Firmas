from pathlib import Path

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15


def main():
    clave_publica = RSA.import_key(Path("medisoft_pub.pem").read_bytes())
    contenido = Path("SHA256SUMS.txt").read_bytes()
    firma = Path("SHA256SUMS.sig").read_bytes()

    resumen = SHA256.new(contenido)

    try:
        pkcs1_15.new(clave_publica).verify(resumen, firma)
        print("La firma es valida.")
    except (ValueError, TypeError):
        print("La firma no es valida.")


if __name__ == "__main__":
    main()
