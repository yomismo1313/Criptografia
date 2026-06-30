# Criptografia
🔐 Writeup — Ejercicio de Criptografía Aplicada


Escalada progresiva a través de 30 usuarios usando codificaciones, cifrados clásicos, OpenSSL, RSA/AES, funciones hash e ingeniería inversa de un cifrado XOR personalizado.



Entorno: Kali Linux → Ubuntu (10.0.2.12) · Herramientas: openssl, hashcat, hash-identifier, cryptii.com, dcode.fr


📁 Estructura del repositorio

.
├── README.md                              # Este writeup completo
├── scripts/
│   ├── xor_descifrar.py                   # Descifrado del reto encrypt8 (XOR)
│   └── afin_descifrar.py                  # Descifrado del reto encrypt9 (cifrado afín)
└── cripto_repo_screenshots/
    └── screenshots/
        ├── page_01.png ... page_16.png    # Capturas de cada paso, en orden


📋 Tabla de credenciales
## Encoding (encode1–encode8)

| Reto     | Usuario/Contraseña | Técnica                                              |
|----------|---------------------|-------------------------------------------------------|
| encode1  | encode1             | Texto plano en `info.txt`                             |
| encode2  | revers3D            | Texto invertido (rev)                                  |
| encode3  | B4se64              | Base64                                                  |
| encode4  | D3sreveR46es4B       | Base64 invertido                                       |
| encode5  | H3xToT3xt            | Hexadecimal → ASCII (`xxd -r -p`)                       |
| encode6  | ASD3cimal           | Decimal → ASCII (CI) (cryptii.com)                     |
| encode7  | URL<'#'>Encoding    | URL Encoding (cryptii.com)                              |
| encode8  | Text2Binary         | Binario → texto (cryptii.com)                           |

## Encrypt (encrypt1–encrypt9)

| Reto      | Usuario/Contraseña    | Técnica                                                |
|-----------|------------------------|---------------------------------------------------------|
| encrypt1  | encrypt1               | Texto plano en `flag_mid.txt`                           |
| encrypt2  | CaesarKn0w             | Cifrado César, 17 posiciones                             |
| encrypt3  | SustituyeME             | Sustitución alfabética                                   |
| encrypt4  | NotSoEasy               | Transposición columnar (clave `TRANSPOSE`)               |
| encrypt5  | EncryptIT               | Cifrado Vigenère (clave `Vigenere`)                       |
| encrypt6  | 3DESEncription!         | OpenSSL 3DES (pass `Symmetric`)                           |
| encrypt7  | AESEncrypt256           | OpenSSL AES-256-CBC (pass `AES256Symmetric`)               |
| encrypt8  | -H@rdl3v3l!!            | Texto plano en `credentials.txt` (vía hashing6)            |
| encrypt9  | anagrama:amargana       | Ingeniería inversa de `xor.py`                            |

## PK Encrypt (pkencrypt1–pkencrypt3)

| Reto       | Usuario/Contraseña | Técnica                                                       |
|------------|----------------------|------------------------------------------------------------------|
| pkencrypt1 | pkencrypt1           | Texto plano en `flag_mid.txt`                                    |
| pkencrypt2 | Dec0deASPrivate       | RSA directo (`openssl pkeyutl -decrypt`)                          |
| pkencrypt3 | KeyExchangeEPH        | Cifrado híbrido RSA + AES (clave efímera)                         |

## Hashing (hashing1–hashing6)

| Reto      | Usuario/Contraseña                  | Técnica                                              |
|-----------|---------------------------------------|---------------------------------------------------------|
| hashing1  | hashing1                              | Texto plano en `flag_mid.txt`                            |
| hashing2  | Check1ngMD5                           | Hash MD5 → coincide con `contraseña7.txt`                |
| hashing3  | Check1ngSHA1                          | Hash SHA-1 → coincide con `contraseña4.txt`              |
| hashing4  | BDHey23dsfad890bSHDYsm                | Hash SHA-256 → coincide con `contraseña8.txt`            |
| hashing5  | BDHasDFHsydnbSHDYsm                   | Hash SHA-512 → coincide con `contraseña9.txt`            |
| hashing6  | admin123                              | Fuerza bruta MD5 con hashcat                              |

🗺️ Flujo general del reto

ubuntu (10.0.2.12)
  │
  ├─ Codificaciones (encode1 → encode8)
  │    rev → base64 → base64 invertido → hex → decimal → URL encoding → binario
  │
  ├─ Cifrados clásicos (encrypt1 → encrypt5)
  │    César → sustitución alfabética → transposición → Vigenère
  │
  ├─ Cifrado simétrico OpenSSL (encrypt5 → encrypt7)
  │    3DES → AES-256-CBC
  │
  ├─ Cifrado asimétrico / híbrido (pkencrypt1 → pkencrypt3)
  │    RSA directo → híbrido RSA+AES (clave efímera)
  │
  ├─ Funciones hash (hashing1 → hashing6)
  │    MD5 → SHA-1 → SHA-256 → SHA-512 → hashcat (MD5)
  │
  └─ Ingeniería inversa (encrypt8 → encrypt9)
       XOR + Base64 invertido + ruido aleatorio → cifrado afín hexadecimal


0. Acceso inicial

Desde Kali, en la misma red NAT, se descubre la máquina víctima con arp-scan:

bashsudo arp-scan --interface=eth0 --localnet

Se identifica la IP 10.0.2.12 (Ubuntu). Conexión vía SSH con credenciales por defecto:

bashssh ubuntu@10.0.2.12
# password: ubuntu

ls -la y cat info.txt revelan en texto plano las credenciales del primer usuario: encode1 / encode1.

Mostrar imagen


1. Cadena de codificaciones (encode1 → encode8)

encode1 → encode2 — Texto invertido

cat contraseña.txt muestra la frase invertida. Se revierte con rev:

bashecho "D3srever se 2edocne ed añesartnoc aL" | rev
# → La contraseña de encode2 es revers3D

encode2 → encode3 — Base64

bashecho "TGEgY29udHJhc2XDsWEgZGUgZW5jb2RlMyBlcyBCNHNlNjQK" | base64 -d
# → La contraseña de encode3 es B4se64

encode3 → encode4 — Base64 invertido

El contenido está invertido y en Base64. Se aplica rev y luego base64 -d:

bashcat contraseña.txt | rev | base64 --decode
# → La contraseña de encode4 es D3sreveR46es4B

Mostrar imagen

encode4 → encode5 — Hexadecimal

bashecho "4C 61 20 63 6F 6E ... 78 74" | xxd -r -p
# → La contraseña de encode5 es H3xToT3xt

encode5 → encode6 — Decimal

contraseña.txt contiene códigos ASCII en decimal. Se decodifica en cryptii.com seleccionando "Entero → Descifrar":

76 97 32 99 111 110 116 ... → La contraseña de encode6 es ASD3cimalCI

Mostrar imagen

encode6 → encode7 — URL Encoding

La%20contrase%C3%B1a%20de%20encode7%20es%20URL%3C%27%23%27%3EEncoding

Decodificado en cryptii.com (Url encoding → Descifrar):

→ La contraseña de encode7 es URL<'#'>Encoding

encode7 → encode8 — Binario

contraseña.txt contiene una larga cadena binaria. Decodificado en cryptii.com (Binary → Integer → Text):

→ La contraseña de encode8 es Text2Binary

Mostrar imagen

encode8 — flag_mid.txt

bashcd /home/encode8 && cat flag_mid.txt
# Continua con los ejercicios de cifrado
# Usuario: encrypt1 / Contraseña: encrypt1


2. Cifrados clásicos (encrypt1 → encrypt5)

encrypt1 → encrypt2 — Cifrado César

bashcat contraseña.txt
# Cr tfekirjvñr uv vetipgk2 vj TrvjriBe0n

Decodificado en cryptii.com con "Caesar cipher", desplazamiento de 17 posiciones:

→ La contraseña de encrypt2 es CaesarKn0w

Mostrar imagen

encrypt2 → encrypt3 — Sustitución alfabética

Se proporcionan ejemplo.txt y ejemplo.txt.enc. Comparando ambos carácter a carácter se reconstruye la tabla de sustitución:

Alfabeto originalABCDEFILMNOPQRSTUYAlfabeto cifradoUVWXYZFIJKLCDEOPQM

Con esta tabla en cryptii.com ("Alphabetical substitution → Decode"):

→ La contraseña de encrypt3 es SustituyeME

Mostrar imagen

encrypt3 → encrypt4 — Transposición columnar

info.txt indica la clave TRANSPOSE. Resolución manual:


Se asigna a cada letra de TRANSPOSE su número de orden alfabético: T=20 R=18 A=1 N=14 S=19 P=16 O=15 S=19 E=5
Se ordenan las columnas de menor a mayor y se distribuye el texto cifrado.
Se reordenan las columnas a su posición original y se lee fila por fila.


Resultado: "La pass de encrypt4 es NotSoEasy"

Mostrar imagen

encrypt4 → encrypt5 — Cifrado Vigenère

info.txt ofrece varios candidatos. Probando Vigenère con clave Vigenere en cryptii.com:

Gi vefw ui zvivltk5 in MtgecgxDBBmtieimm
→ La pass de encrypt5 es EncryptITVigenere

Mostrar imagen


3. Cifrado simétrico con OpenSSL (encrypt5 → encrypt7)

encrypt5 → encrypt6 — 3DES

contraseña.txt.des3 comienza por Salted__, indicando cifrado con openssl enc. La contraseña correcta entre los candidatos de info.txt es Symmetric:

bashopenssl enc -d -des3 -pbkdf2 -in contraseña.txt.des3 -out contraseña_descifrada.txt -k Symmetric
cat contraseña_descifrada.txt
# → La contraseña de encrypt6 es 3DESEncription!

encrypt6 → encrypt7 — AES-256-CBC

contraseña.txt.aes2 también comienza por Salted__. La contraseña correcta es AES256Symmetric:

bashopenssl enc -aes-256-cbc -pbkdf2 -d -in contraseña.txt.aes2 -out contraseña_descifrada.txt -k AES256Symmetric
cat contraseña_descifrada.txt
# → La contraseña de encrypt7 es AESEncrypt256

Mostrar imagen

encrypt7 — flag_mid.txt

bashcat flag_mid.txt
# Continua con los ejercicios de cifrado asimétrico
# Usuario: pkencrypt1 / Contraseña: pkencrypt1


4. Cifrado asimétrico e híbrido (pkencrypt1 → pkencrypt3)

pkencrypt1 → pkencrypt2 — RSA directo

pkencrypt1 dispone de contraseña.txt.enc y un directorio keys/ con privada.pem y publica.pem. Se descifra con la clave privada:

bashopenssl pkeyutl -decrypt -inkey keys/privada.pem \
  -in contraseña.txt.enc -out contraseña_descifrada.txt
cat contraseña_descifrada.txt
# → La contraseña de pkencrypt2 es Dec0deASPrivate

pkencrypt2 → pkencrypt3 — Cifrado híbrido RSA + AES

pkencrypt2 contiene contraseña.txt.aes2, ephemereal_key.enc y otro par de claves RSA. Esquema híbrido: clave AES efímera cifrada con RSA, datos cifrados con esa clave AES.

Paso 1 — recuperar la clave AES con RSA:

bashopenssl pkeyutl -decrypt -inkey keys/privada.pem \
  -in ephemereal_key.enc -out ephemereal_key_descifrada.txt
cat ephemereal_key_descifrada.txt
# → VyX76Dnmsny6534jjDM

Paso 2 — descifrar el fichero AES con esa clave:

bashopenssl enc -aes-256-cbc -pbkdf2 -d \
  -pass file:ephemereal_key_descifrada.txt \
  -in contraseña.txt.aes2 -out contraseña.txt.aes2_descifrada.txt
cat contraseña.txt.aes2_descifrada.txt
# → La contraseña de pkencrypt3 es KeyExchangeEPH

Mostrar imagen

pkencrypt3 — flag_mid.txt y bifurcación

Si has llegado hasta aquí, se abre una nueva vía en el reto. Tú eliges:
  - Seguir con cifrado asimétrico → analiza contraseña.txt.enc
  - Arrancar con funciones hash  → Usuario: hashing1 / Contraseña: hashing1

Este writeup continúa por la rama de funciones hash.


5. Funciones hash (hashing1 → hashing6)

El patrón en hashing1 → hashing4: info.txt da un hash, hay que encontrar cuál de los diez ficheros contraseña1.txt ... contraseña10.txt en /Creds lo produce. Solo se pueden probar 2 candidatos antes de bloquear el usuario, así que primero se identifica el tipo con hash-identifier.

hashing1 → hashing2 — MD5

bashhash-identifier 9f75f653a20dba0796f5011dddc34aaa
# → MD5
md5sum Creds/contraseña*.txt
# contraseña7.txt coincide
cat Creds/contraseña7.txt
# → La pass de hashing2 es Check1ngMD5

Mostrar imagen

hashing2 → hashing3 — SHA-1

bashhash-identifier 26ed6139d311e851d4efa906bfc78e90f970cedd
# → SHA-1
sha1sum Creds/contraseña*.txt
# contraseña4.txt coincide
cat Creds/contraseña4.txt
# → La pass de hashing3 es Check1ngSHA1

Mostrar imagen

hashing3 → hashing4 — SHA-256

bashsha256sum Creds/contraseña*.txt
# contraseña8.txt coincide
cat Creds/contraseña8.txt
# → La contraseña de hashing4 es BDHey23dsfad890bSHDYsm

Mostrar imagen

hashing4 → hashing5 — SHA-512

bashhash-identifier 8a2f1de3b96eac2e0687ab9980d450b147aa3cb4...
# → SHA-512
sha512sum Creds/contraseña*.txt
# contraseña9.txt coincide
cat Creds/contraseña9.txt
# → La contraseña de hashing5 es BDHasDFHsydnbSHDYsm

hashing5 → hashing6 — Fuerza bruta MD5 con hashcat

hashing5 contiene contraseña_hashing6.md5 con un hash MD5 sin texto plano conocido:

bashhash-identifier 0192023a7bbd73250516f069df18b500
# → MD5

hashcat -m 0 -a 0 hash.txt /usr/share/wordlists/rockyou.txt
hashcat -m 0 hash.txt --show
# 0192023a7bbd73250516f069df18b500:admin123


La contraseña de hashing6 resultante del crackeo es admin123.



Mostrar imagen

hashing6 — credentials.txt

bashcat credentials.txt
# user: encrypt8
# password: -H@rdl3v3l!!

Mostrar imagen


6. Ingeniería inversa de un cifrado XOR (encrypt8 → encrypt9)

encrypt8 contiene secret.txt, secret_1.txt, y los scripts xor.py, xorcopy.py y xorcopy.py.save (copias de trabajo del mismo cifrador). El script xor.py es el que genera los ficheros cifrados:

python#!/usr/bin/python3
import base64
import random

def xorEncryption(key, plaintext):
    ciphertext = ""
    for i in range(len(plaintext)):
        ciphertext += chr(ord(plaintext[i]) ^ ord(key[i]))
    ciphertext = base64.b64encode(bytes(ciphertext, encoding="utf-8")).decode()[::-1]
    random_bytes = base64.b64encode(bytes(chr(random.randint(0, 255)), encoding="utf-8")).decode()
    ciphertext = random_bytes + ciphertext + random_bytes
    return ciphertext

if __name__ == '__main__':
    f = open("/root/secreto.txt")
    secreto = f.read()
    secreto = secreto.strip()
    ciphertext = xorEncryption("abcdefgh:12345678", secreto)
    f = open("./secret.txt", "w")
    f.write(ciphertext + "\n")
    f.close()

Es decir: el script lee un texto plano de /root/secreto.txt, lo cifra con la clave abcdefgh:12345678 y guarda el resultado en secret.txt. Esto confirma la clave de cifrado que se necesita para revertir el proceso.

Lógica de cifrado (pasos en orden):


XOR del texto plano con la clave abcdefgh:12345678
Codificación en Base64
Inversión de la cadena Base64
Se añaden 4 bytes aleatorios (ruido) al inicio y al final


Para descifrar se invierte el proceso:
quitar ruido (4 chars a cada lado) → invertir cadena → decodificar Base64 → XOR con la misma clave.

El script de descifrado está disponible en scripts/xor_descifrar.py:

pythonimport base64

with open("secret.txt", "r") as f:
    data = f.read().strip()

# Quitar los 4 caracteres de ruido en cada extremo
core = data[4:-4]

# Invertir la cadena
rev = core[::-1]

# Decodificar Base64
decoded = base64.b64decode(rev).decode("utf-8")

# Clave usada en el XOR original
key = "abcdefgh:12345678"

# Descifrar con XOR
plaintext = ""
for i in range(len(decoded)):
    plaintext += chr(ord(decoded[i]) ^ ord(key[i % len(key)]))

print("Texto original:", plaintext)

bashpython3 scripts/xor_descifrar.py
# Texto original: anagrama:amargana

encrypt9 — Cifrado afín hexadecimal

encrypt9 contiene msg2.enc (cadena hexadecimal) y un script chall_crypto.py que falla con:

ModuleNotFoundError: No module named 'secretfile'

En lugar de reparar el script, se deduce la transformación afín inversa byte a byte y se descifra directamente desde la terminal con scripts/afin_descifrar.py:

bashpython3 -c "
ct = open('msg2.enc').read().strip()
print(' '.join(chr(((b - 18) * 179) % 256) for b in bytes.fromhex(ct)))
"

O bien con el script ya preparado:

bashpython3 scripts/afin_descifrar.py

Lo conseguiste! Aplica ROT5 a tu nombre y escríbelo por slack!

Mostrar imagen


🛠️ Herramientas utilizadas

HerramientaUso en este retocryptii.comDecimal, URL Encoding, Binario, César, Sustitución, Vigenèredcode.frApoyo para identificación y análisis de cifrados clásicoshash-identifierIdentificación del tipo de hash (MD5, SHA-1, SHA-256, SHA-512)hashcatAtaque de diccionario contra hashes MD5opensslDescifrado simétrico (3DES, AES-256-CBC) y asimétrico (RSA, pkeyutl)xxdConversión hexadecimal → ASCIIrevInversión de cadenas de textobase64Codificación/decodificación Base64


📝 Conclusión

Este reto recorre de forma progresiva el espectro completo de la criptografía aplicada: desde codificaciones triviales (Base64, hexadecimal, binario, URL encoding) hasta cifrados clásicos (César, sustitución, transposición, Vigenère), pasando por cifrado simétrico moderno (3DES y AES-256 vía OpenSSL), cifrado híbrido asimétrico (RSA + AES con clave efímera), funciones hash (MD5, SHA-1/256/512) con verificación por fuerza bruta, y finalmente ingeniería inversa de un esquema XOR personalizado y un cifrado afín hexadecimal sin el script original.

La progresión refleja de forma didáctica la evolución histórica y técnica de la criptografía, y refuerza la importancia de saber identificar un esquema de cifrado a partir de sus artefactos: prefijos como Salted__, estructura de claves RSA, patrones en Base64, etc.


⚠️ Disclaimer

Este writeup documenta un ejercicio realizado en un entorno de laboratorio controlado y aislado con fines educativos (formación en criptografía aplicada / CTF). No reproduzcas estas técnicas contra sistemas sin autorización explícita del propietario.


Cada cifrado roto es una puerta que se abre. Este reto nació para que cualquiera pueda cruzarlas. 🔑
