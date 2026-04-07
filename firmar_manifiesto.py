from pathlib import Path

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15


def main():
    contenido = Path("SHA256SUMS.txt").read_bytes()
    clave_privada = RSA.import_key(Path("medisoft_priv.pem").read_bytes())

    resumen = SHA256.new(contenido)
    firma = pkcs1_15.new(clave_privada).sign(resumen)

    Path("SHA256SUMS.sig").write_bytes(firma)

    print("Se genero SHA256SUMS.sig")


if __name__ == "__main__":
    main()
