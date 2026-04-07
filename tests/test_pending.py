import hashlib
from pathlib import Path

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

from consultar_hibp import sha1_texto, sha256_texto
from explorar_hashes import calcular_hash, contar_bits_distintos
from generar_manifiesto import sha256_archivo


def test_sha256_de_admin():
    assert sha256_texto("admin") == "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"


def test_sha1_de_admin():
    assert sha1_texto("admin") == "D033E22AE348AEB5660FC2140AEC35850C4DA997"


def test_bits_distintos_en_sha256():
    hash_a = calcular_hash("MediSoft-v2.1.0", hashlib.sha256)
    hash_b = calcular_hash("medisoft-v2.1.0", hashlib.sha256)
    assert contar_bits_distintos(hash_a, hash_b) == 120


def test_sha256_archivo(tmp_path):
    archivo = tmp_path / "demo.txt"
    archivo.write_text("hola mundo", encoding="utf-8")

    esperado = hashlib.sha256(b"hola mundo").hexdigest()
    assert sha256_archivo(archivo) == esperado


def test_firma_rsa():
    clave = RSA.generate(2048)
    contenido = b"contenido del manifiesto"
    resumen = SHA256.new(contenido)

    firma = pkcs1_15.new(clave).sign(resumen)

    pkcs1_15.new(clave.publickey()).verify(resumen, firma)
