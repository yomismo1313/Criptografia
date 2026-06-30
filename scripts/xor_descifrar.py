#!/usr/bin/python3
"""
xor_descifrar.py

Script de descifrado para el reto encrypt8 del ejercicio de criptografía.

El cifrado original (xor.py) aplica estos pasos:
  1. XOR del texto plano con la clave "abcdefgh:12345678"
  2. Codificación en Base64
  3. Inversión de la cadena Base64
  4. Se añaden 4 bytes aleatorios (ruido) al principio y al final

Este script invierte cada paso en orden contrario:
  1. Quitar el ruido (4 caracteres a cada lado)
  2. Invertir la cadena
  3. Decodificar Base64
  4. XOR con la misma clave

Uso:
    python3 xor_descifrar.py
"""

import base64

INPUT_FILE = "secret.txt"
KEY = "abcdefgh:12345678"


def descifrar(data: str, key: str) -> str:
    # Los primeros y últimos 4 caracteres son ruido aleatorio en Base64
    core = data[4:-4]

    # Invertir la cadena
    rev = core[::-1]

    # Decodificar Base64
    decoded = base64.b64decode(rev).decode("utf-8")

    # Descifrar usando XOR con la clave repetida cíclicamente
    plaintext = ""
    for i in range(len(decoded)):
        plaintext += chr(ord(decoded[i]) ^ ord(key[i % len(key)]))

    return plaintext


if __name__ == "__main__":
    with open(INPUT_FILE, "r") as f:
        data = f.read().strip()

    plaintext = descifrar(data, KEY)
    print("Texto original:", plaintext)
