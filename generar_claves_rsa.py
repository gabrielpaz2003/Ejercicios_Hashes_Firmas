from pathlib import Path

from Crypto.PublicKey import RSA


def main():
    clave = RSA.generate(2048)

    Path("medisoft_priv.pem").write_bytes(clave.export_key())
    Path("medisoft_pub.pem").write_bytes(clave.publickey().export_key())

    print("Se genero medisoft_priv.pem")
    print("Se genero medisoft_pub.pem")


if __name__ == "__main__":
    main()
