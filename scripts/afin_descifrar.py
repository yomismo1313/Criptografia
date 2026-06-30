#!/usr/bin/python3
"""
afin_descifrar.py

Script de descifrado para el reto encrypt9 del ejercicio de criptografía.

El fichero msg2.enc contiene una cadena hexadecimal cifrada con un cifrado
afín a nivel de byte: c = (m * a + b) mod 256

El script original (chall_crypto.py) no podía ejecutarse porque importaba
una variable inexistente desde un módulo "secretfile". En vez de reparar
el script, se dedujo la transformación afín inversa byte a byte y se
descifró directamente.

La transformación inversa aplicada es:
    m = ((c - 18) * 179) mod 256

Uso:
    python3 afin_descifrar.py
"""

INPUT_FILE = "msg2.enc"


def descifrar(ciphertext_hex: str) -> str:
    data = bytes.fromhex(ciphertext_hex)
    plaintext = "".join(chr(((b - 18) * 179) % 256) for b in data)
    return plaintext


if __name__ == "__main__":
    with open(INPUT_FILE, "r") as f:
        ciphertext_hex = f.read().strip()

    mensaje = descifrar(ciphertext_hex)
    print(mensaje)
