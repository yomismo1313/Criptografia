🔐 Lab de Criptografía — Escalada de Privilegios
Writeup completo de un laboratorio de criptografía en el que se escala privilegios entre 25 usuarios de una máquina Ubuntu, resolviendo retos de codificación, cifrado simétrico/asimétrico, hashing e ingeniería inversa, apoyándonos en herramientas como `openssl`, `hashcat`, `hash-identifier` y las webs cryptii.com y dcode.fr.
---
📋 Índice
Reconocimiento y acceso inicial
Bloque ENCODE — Codificaciones (encode1 → encode8)
Bloque ENCRYPT — Cifrados simétricos (encrypt1 → encrypt7)
Bloque PKENCRYPT — Cifrado asimétrico (pkencrypt1 → pkencrypt3)
Bloque HASHING — Funciones hash (hashing1 → hashing6)
Bloque final — XOR e ingeniería inversa (encrypt8 → encrypt9)
Resumen de credenciales
Herramientas utilizadas
---
1. Reconocimiento y acceso inicial
Paso 1.1 — Escaneo de la red
Desde Kali Linux, conectada a la misma red NAT que la máquina víctima, identificamos los hosts activos con `arp-scan`:
```bash
sudo arp-scan --interface=eth0 --localnet
```
Esto nos revela la IP de la máquina víctima Ubuntu: `10.0.2.12`
![Escaneo de red con arp-scan](assets/page-01.jpg)
Paso 1.2 — Conexión SSH
Nos conectamos por SSH al usuario `ubuntu` (credenciales conocidas de antemano: `ubuntu`/`ubuntu`):
```bash
ssh ubuntu@10.0.2.12
# Password: ubuntu
```
Paso 1.3 — Primer fichero en texto plano
Listamos el contenido del directorio personal y leemos `info.txt`:
```bash
ls -la
cat info.txt
```
El fichero nos explica la dinámica del reto (codificación → cifrado simétrico → funciones hash) y nos da las primeras credenciales:
```
Usuario: encode1
Pass:    encode1
```
![Contenido de info.txt con las primeras credenciales](assets/page-01.jpg)
---
2. Bloque ENCODE — Codificaciones
> **Objetivo de este bloque:** ir descifrando una cadena de codificaciones (no cifrados criptográficos reales, sino transformaciones reversibles) para saltar de usuario en usuario.
encode1 → encode2 (Texto invertido)
Accedemos a `encode1` (pass `encode1`) y leemos `contraseña.txt`. El texto aparece invertido carácter a carácter:
```bash
su encode1
cat contraseña.txt
# D3srever se 2edocne ed añesartnoc aL
```
Lo revertimos con el comando `rev`:
```bash
echo "D3srever se 2edocne ed añesartnoc aL" | rev
# La contraseña de encode2 es revers3D
```
![Texto invertido y descifrado con rev](assets/page-02.jpg)
Resultado: `encode2` / `revers3D`
---
encode2 → encode3 (Base64)
Accedemos a `encode2` y el fichero `contraseña.txt` contiene una cadena en Base64:
```bash
echo "TGEgY29udHJhc2XDsWEgZGUgZW5jb2RlMyBlcyBCNHNlNjQK" | base64 -d
# La contraseña de encode3 es B4se64
```
Resultado: `encode3` / `B4se64`
---
encode3 → encode4 (Base64 invertido)
En `encode3`, el contenido está codificado en Base64 y además invertido (los caracteres del Base64 al revés). Hay que invertir la cadena antes de decodificar:
```bash
echo "<cadena>" | rev | base64 --decode
# La contraseña de encode4 es D3sreveR46es4B
```
![Base64 invertido descifrado en dos pasos](assets/page-02.jpg)
Resultado: `encode4` / `D3sreveR46es4B`
---
encode4 → encode5 (Hexadecimal)
En `encode4`, el texto está en hexadecimal. Lo convertimos a ASCII con `xxd`:
```bash
echo "4C 61 20 63 6F 6E 74 72 61 73 65 F1 61 20 64 65 20 65 6E 63 6F 64 65 35 20 65 73 20 48 33 78 54 6F 54 33 78 74" | xxd -r -p
# La contraseña de encode5 es H3xToT3xt
```
![Hexadecimal decodificado con xxd](assets/page-02.jpg)
Resultado: `encode5` / `H3xToT3xt`
---
encode5 → encode6 (Decimal / CI — Character Integer)
En `encode5`, el fichero contiene una secuencia de números decimales, cada uno representando el código ASCII de un carácter:
```bash
cat contraseña.txt
# 76 97 32 99 111 110 116 114 97 115 101 195 177 97 32 100 ...
```
Lo resolvemos en cryptii.com, seleccionando la vista "Integer" (8-bit unsigned) → Texto:
Resultado: `encode6` / `ASD3cimalCI`
![Decodificación decimal/entero en cryptii.com](assets/page-03.jpg)
---
encode6 → encode7 (URL Encoding)
En `encode6`, el contenido tiene formato `%XX` típico de URL Encoding:
```
La%20contrase%C3%B1a%20de%20encode7%20es%20URL%3C%27%23%27%3EEncoding
```
Lo resolvemos en cryptii.com con el módulo "URL encoding" → Decode:
Resultado: `encode7` / `URL<'#'>Encoding`
![URL Decoding en cryptii.com](assets/page-03.jpg)
---
encode7 → encode8 (Binario)
En `encode7`, el fichero `contraseña.txt` contiene una cadena binaria:
```
01001100 01100001 00100000 01100011 01101111 01101110 01110100 ...
```
La resolvemos en cryptii.com seleccionando "Binary" → Texto:
Resultado: `encode8` / `Text2Binary`
![Decodificación binaria en cryptii.com](assets/page-04.jpg)
---
encode8 → encrypt1 (Fin del bloque ENCODE)
En `encode8`, encontramos el fichero `flag_mid.txt` que marca el final del bloque de codificación y el inicio del bloque de cifrado:
```bash
cd encode8
cat flag_mid.txt
```
```
Continua con los ejercicios de cifrado
        - Usuario: encrypt1
        - Contraseña: encrypt1
```
![Flag intermedia con las credenciales de encrypt1](assets/page-04.jpg)
---
3. Bloque ENCRYPT — Cifrados simétricos
> **Objetivo de este bloque:** trabajar con cifrados criptográficos reales (César, sustitución, transposición, Vigenère, 3DES, AES) en lugar de simples codificaciones.
encrypt1 → encrypt2 (Cifrado César)
En `encrypt1`, el fichero `contraseña.txt` contiene:
```
Cr tfekirjvñr uv vetipgk2 vj TrvjriBe0n
```
Lo identificamos como un cifrado César. Lo resolvemos en cryptii.com con el módulo "Caesar cipher", probando desplazamientos hasta dar con 17 posiciones:
Resultado: `encrypt2` / `CaesarKn0w`
![Descifrado César con 17 posiciones en cryptii.com](assets/page-04.jpg)
---
encrypt2 → encrypt3 (Sustitución alfabética)
En `encrypt2` encontramos dos ficheros de referencia, `ejemplo.txt` (texto plano) y `ejemplo.txt.enc` (su versión cifrada), que nos sirven para deducir el alfabeto de sustitución comparando letra a letra:
```bash
cat ejemplo.txt ejemplo.txt.enc
```
```
Esto es un texto de prueba para confirmar que funciona bien el cifrado de sustitucion y que es robusto
Yopl yo qk pytpl xy ceqyvu cueu wlkzfejue dqy zqkwflku vfyk yi wfzeuxl xy oqopfpqwflk m dqy yo elvqopl
```
Comparando carácter a carácter reconstruimos la tabla de sustitución:
Alfabeto Simple	A	B	C	D	E	F	I	L	M	N	O	P	Q	R	S	T	U	Y
Alfabeto Cifrado	U	V	W	X	Y	Z	F	I	J	K	L	C	D	E	O	P	Q	M
![Deducción de la tabla de sustitución comparando ficheros](assets/page-05.jpg)
Aplicamos esta tabla en cryptii.com (módulo "Alphabetical substitution") sobre `contraseña.txt.enc`:
Resultado: `encrypt3` / `SustituyeME`
![Descifrado por sustitución alfabética en cryptii.com](assets/page-05.jpg)
---
encrypt3 → encrypt4 (Transposición columnar)
En `encrypt3`, el fichero `info.txt` nos avisa de que es un cifrado por transposición y sugiere que la clave podría ser `TRANSPOSE`:
```bash
cat info.txt
# Parece que el fichero ha sido cifrado mediante un algoritmo de Transposición.
# ¿Podrías verificar si la clave de cifrado es TRANSPOSE?
```
![Pista de transposición columnar con clave TRANSPOSE](assets/page-05.jpg)
Resolución manual paso a paso
1. Numeramos el abecedario del 1 al 26:
```
A=1 B=2 C=3 D=4 E=5 F=6 G=7 H=8 I=9 J=10 K=11 L=12 M=13
N=14 O=15 P=16 Q=17 R=18 S=19 T=20 U=21 V=22 W=23 X=24 Y=25 Z=26
```
2. Asignamos el número correspondiente a cada letra de la clave `TRANSPOSE`:
T	R	A	N	S	P	O	S	E
20	18	1	14	19	16	15	19	5
3. Ordenamos las columnas de menor a mayor número y colocamos el texto cifrado por filas:
1	5	14	15	16	18	19	19	20
A	E	N	O	P	R	S	S	T
p	r	a	d	s	a	s	e	L
r	s	y	4	t	c	p	e	n
t	v	S	a	E	o	o	s	N
4. Devolvemos las columnas a su orden original según la clave `TRANSPOSE`:
T	R	A	N	S	P	O	S	E
20	18	1	14	19	16	15	19	5
L	a	p	a	s	s	d	e	e
n	c	r	y	p	t	4	e	s
N	o	t	S	o	E	a	s	y
5. Leemos de izquierda a derecha, fila por fila:
```
Lapassdeencryt4esNotSoEasy
```
Añadiendo los espacios correspondientes:
```
La pass de encrypt4 es NotSoEasy
```
![Tablas de descifrado manual de la transposición columnar](assets/page-06.jpg)
Resultado: `encrypt4` / `NotSoEasy`
---
encrypt4 → encrypt5 (Cifrado Vigenère)
En `encrypt4`, el fichero `info.txt` nos da cuatro posibles claves a probar:
```bash
cat info.txt
# ¿Podrías verificar si la contraseña es alguna de las siguientes?
# - Caesar
# - AlKindi
# - Vigenere
# - Enigma
```
![Pista con cuatro posibles claves de cifrado](assets/page-06.jpg)
Probamos la clave `Vigenere` en cryptii.com (módulo "Vigenère cipher") sobre `contraseña.txt.enc`:
Resultado: `encrypt5` / `EncryptITVigenere`
![Descifrado Vigenère con clave Vigenere en cryptii.com](assets/page-07.jpg)
---
encrypt5 → encrypt6 (OpenSSL 3DES)
En `encrypt5`, el fichero `contraseña.txt.des3` empieza por la cabecera `Salted__`, lo que indica que está cifrado con OpenSSL usando una clave derivada por salt (PBKDF2):
```bash
cat info.txt
# ¿Podrías verificar si la contraseña es alguna de las siguientes?
# - RC4Encryption
# - DES3Rules
# - Symmetric
# - NotSoEasy
```
Probamos descifrar con 3DES y la clave `Symmetric`:
```bash
openssl enc -d -des3 -pbkdf2 -in contraseña.txt.des3 -out contraseña_descifrada.txt -k Symmetric
cat contraseña_descifrada.txt
# La contraseña de encrypt6 es 3DESEncription!
```
![Descifrado 3DES con OpenSSL](assets/page-07.jpg)
Resultado: `encrypt6` / `3DESEncription!`
---
encrypt6 → encrypt7 (OpenSSL AES-256-CBC)
En `encrypt6`, el fichero `contraseña.txt.aes2` también empieza por `Salted__` (OpenSSL), pero esta vez con AES-256-CBC:
```bash
cat info.txt
# ¿Podrías verificar si la contraseña es alguna de las siguientes?
# - RC4Encryption
# - CBCRules
# - NotSoEasy
# - AES256Symmetric
# - Symmetric
# - ZenAES256
```
![Pista con seis posibles claves para AES](assets/page-07.jpg)
Probamos descifrar con AES-256-CBC y la clave `AES256Symmetric`:
```bash
openssl enc -d -aes-256-cbc -pbkdf2 -in contraseña.txt.aes2 -out contraseña_descifrada.txt -k AES256Symmetric
cat contraseña_descifrada.txt
# La contraseña de encrypt7 es AESEncrypt256
```
![Descifrado AES-256-CBC con OpenSSL](assets/page-08.jpg)
Resultado: `encrypt7` / `AESEncrypt256`
---
encrypt7 → pkencrypt1 (Fin del bloque ENCRYPT simétrico)
Accedemos a `encrypt7` y leemos `flag_mid.txt`, que marca el inicio del bloque de criptografía asimétrica:
```bash
cd encrypt7
cat flag_mid.txt
```
```
Continua con los ejercicios de cifrado asimétrico
        - Usuario: pkencrypt1
        - Contraseña: pkencrypt1
```
![Flag intermedia con credenciales de pkencrypt1](assets/page-08.jpg)
---
4. Bloque PKENCRYPT — Cifrado asimétrico
> **Objetivo de este bloque:** trabajar con criptografía de clave pública/privada RSA, incluyendo cifrado híbrido (RSA + AES).
pkencrypt1 → pkencrypt2 (RSA directo)
En `pkencrypt1` encontramos `contraseña.txt.enc` y un directorio `keys/` con clave pública y privada:
```bash
ls
# contraseña.txt.enc  keys

ls keys/
# privada.pem  publica.pem
```
Desciframos directamente con la clave privada RSA:
```bash
openssl pkeyutl -decrypt -inkey keys/privada.pem -in contraseña.txt.enc -out contraseña_descifrada.txt
cat contraseña_descifrada.txt
# La contraseña de pkencrypt2 es Dec0deASPrivate
```
![Descifrado RSA directo con openssl pkeyutl](assets/page-08.jpg)
Resultado: `pkencrypt2` / `Dec0deASPrivate`
---
pkencrypt2 → pkencrypt3 (Cifrado híbrido RSA + AES)
En `pkencrypt2` encontramos tres elementos: `contraseña.txt.aes2`, `ephemereal_key.enc` y un directorio `keys/`. Esto es un cifrado híbrido: el mensaje está cifrado con AES usando una clave simétrica efímera, y esa clave efímera está a su vez cifrada con RSA.
```bash
ls
# contraseña.txt.aes2  ephemereal_key.enc  keys

ls keys/
# privada.pem  publica.pem
```
![Estructura del cifrado híbrido RSA+AES](assets/page-08.jpg)
Paso 1 — Recuperar la clave AES efímera con RSA:
```bash
openssl pkeyutl -decrypt -inkey keys/privada.pem -in ephemereal_key.enc -out ephemereal_key_descifrada.txt
cat ephemereal_key_descifrada.txt
# VyX76Dnmsny6534jjDM
```
Paso 2 — Usar esa clave para descifrar el AES:
```bash
openssl enc -aes-256-cbc -pbkdf2 -d --pass file:ephemereal_key_descifrada.txt -in contraseña.txt.aes2 -out contraseña.txt.aes2_descifrada.txt
cat contraseña.txt.aes2_descifrada.txt
# La contraseña de pkencrypt3 es KeyExchangeEPH
```
![Descifrado en dos fases: RSA recupera la clave AES efímera](assets/page-09.jpg)
Resultado: `pkencrypt3` / `KeyExchangeEPH`
---
pkencrypt3 → hashing1 (Bifurcación del reto)
En `pkencrypt3`, el fichero `flag_mid.txt` nos da a elegir entre dos caminos: seguir en criptografía asimétrica o saltar al bloque de hashing:
```bash
cd pkencrypt3
cat flag_mid.txt
```
```
Si has llegado hasta aquí, se abre una nueva vía en el reto.

Tú eliges.

- Seguir con los ejercicios de criptografía asimétrica
        - Continúa analizando el fichero contraseña.txt.enc
- Arrancar con los ejercicios de funciones de hash:
        - Usuario: hashing1
        - Contraseña: hashing1
```
![Flag de bifurcación entre asimétrica y hashing](assets/page-09.jpg)
Elegimos continuar por el camino de hashing.
---
5. Bloque HASHING — Funciones hash
> **Objetivo de este bloque:** identificar el tipo de hash y compararlo contra una lista de ficheros candidatos para encontrar cuál coincide (sin romper el hash, solo comparándolo).
Mecánica del bloque
En cada nivel `hashingN`, encontramos:
Un fichero `info.txt` con un hash objetivo
Un directorio `/Creds` con 10 ficheros candidatos (`contraseña1.txt` … `contraseña10.txt`)
El reto consiste en calcular el hash de cada candidato y encontrar cuál coincide con el hash objetivo.
> ⚠️ **Regla importante**: el enunciado avisa de que solo se pueden probar 2 contraseñas como máximo antes de que el usuario se bloquee — por eso es imprescindible identificar primero el hash correcto comparando **todos** los candidatos, en lugar de probar usuarios al azar.
---
hashing1 → hashing2 (MD5)
```bash
cat info.txt
```
```
Sabemos que el fichero que guarda la clave correcta para el usuario hashing2
tiene el siguiente hash: 9f75f653a20dba0796f5011dddc34aaa
```
![Hash objetivo de hashing2](assets/page-09.jpg)
1. Identificamos el tipo de hash con `hash-identifier`:
```bash
hash-identifier 9f75f653a20dba0796f5011dddc34aaa
# Possible Hashs: [+] MD5
```
![hash-identifier detecta MD5](assets/page-10.jpg)
2. Calculamos el MD5 de los 10 candidatos y buscamos coincidencia:
```bash
md5sum Creds/contraseña*.txt
```
El hash de `contraseña7.txt` coincide:
```bash
cat Creds/contraseña7.txt
# La pass de hashing2 es Check1ngMD5
```
![Comparación de hashes MD5 de todos los candidatos](assets/page-10.jpg)
Resultado: `hashing2` / `Check1ngMD5`
---
hashing2 → hashing3 (SHA-1)
```bash
cat info.txt
# Hash objetivo: 26ed6139d311e851d4efa906bfc78e90f970cedd
```
![Hash objetivo de hashing3](assets/page-10.jpg)
`hash-identifier` lo identifica como SHA-1:
```bash
hash-identifier 26ed6139d311e851d4efa906bfc78e90f970cedd
# Possible Hashs: [+] SHA-1
```
![hash-identifier detecta SHA-1](assets/page-11.jpg)
Calculamos SHA-1 de los candidatos:
```bash
sha1sum Creds/contraseña*.txt
```
El hash de `contraseña4.txt` coincide:
```bash
cat Creds/contraseña4.txt
# La pass de hashing3 es Check1ngSHA1
```
Resultado: `hashing3` / `Check1ngSHA1`
---
hashing3 → hashing4 (SHA-256)
```bash
cat info.txt
# Hash objetivo: c5f8d03cab180bffb6268f096ebd44840d5d2f5481a75ad588ca02000f572e7c
```
![Hash objetivo de hashing4](assets/page-11.jpg)
`hash-identifier` lo identifica como SHA-256:
```bash
hash-identifier c5f8d03cab180bffb6268f096ebd44840d5d2f5481a75ad588ca02000f572e7c
# Possible Hashs: [+] SHA-256
```
Calculamos SHA-256 de los candidatos:
```bash
sha256sum Creds/contraseña*.txt
```
El hash de `contraseña8.txt` coincide:
```bash
cat Creds/contraseña8.txt
# La contraseña del usuario hashing4 es BDHey23dsfad890bSHDYsm
```
![Comparación de hashes SHA-256](assets/page-12.jpg)
Resultado: `hashing4` / `BDHey23dsfad890bSHDYsm`
---
hashing4 → hashing5 (SHA-512)
```bash
cat info.txt
# Hash objetivo: 8a2f1de3b96eac2e0687a0998080450b147aa3cb46ac891c724abaf757495518211ac71b16f59b92e7704ab1f6553e6f9609a977f723abca0f29b10089fe5db44
```
![Hash objetivo de hashing5](assets/page-12.jpg)
`hash-identifier` lo identifica como SHA-512:
```bash
hash-identifier <hash>
# Possible Hashs: [+] SHA-512
```
![hash-identifier detecta SHA-512](assets/page-13.jpg)
Calculamos SHA-512 de los candidatos. El hash de `contraseña9.txt` coincide:
```bash
sha512sum Creds/contraseña*.txt
cat Creds/contraseña9.txt
# La contraseña del usuario hashing5 es BDHasDFHsydnbSHDYsm
```
Resultado: `hashing5` / `BDHasDFHsydnbSHDYsm`
---
hashing5 → hashing6 (Fuerza bruta con hashcat)
En `hashing5` encontramos un único fichero, `contraseña_hashing6.md5`:
```bash
cat contraseña_hashing6.md5
# 0192023a7bbd73250516f069df18b500
```
`hash-identifier` confirma que es MD5. Esta vez no hay candidatos que comparar: hay que romper el hash por fuerza bruta con `hashcat`:
```bash
hashcat -m 0 -a 3 0192023a7bbd73250516f069df18b500 ?l?l?l?l?l?l?l?l
```
El ataque revela la contraseña en texto plano:
```
0192023a7bbd73250516f069df18b500:admin123
```
![Hash MD5 roto con hashcat: admin123](assets/page-13.jpg)
Resultado: `hashing6` / `admin123`
---
hashing6 → encrypt8 (credentials.txt)
Accedemos a `hashing6` con la contraseña obtenida (`admin123`) y encontramos `credentials.txt`:
```bash
cd hashing6
cat credentials.txt
```
```
user: encrypt8
password: -H@rdl3v3l!!
```
![Credenciales de encrypt8 en texto plano](assets/page-13.jpg)
Resultado: `encrypt8` / `-H@rdl3v3l!!`
---
6. Bloque final — XOR e ingeniería inversa
encrypt8 (Cifrado XOR)
En `encrypt8` encontramos tres ficheros: dos textos cifrados (`secret.txt`, `secret_1.txt`) y un script de cifrado `xor.py`:
```bash
ls
# secret.txt  secret_1.txt  xor.py  xorcopy.py  xorcopy.py.save

cat secret.txt
# RA==kVWXJlRS9FUAkgCHcxACwAARA=

cat secret_1.txt
# w4Q=kVWXJlRS9FUAkgCHcxACwAAw4Q=
```
![Ficheros cifrados con XOR y el script original](assets/page-13.jpg)
Analizando `xor.py` confirmamos que es un script que cifra (no descifra) usando XOR + Base64 con una clave fija y bytes aleatorios como relleno (padding) al principio y al final:
```python
#!/usr/bin/python3
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
```
![Script xor.py mostrando la lógica de cifrado](assets/page-14.jpg)
Creamos el script inverso `xor_descifrar.py` invirtiendo la lógica (quitar el padding, revertir el Base64, decodificar y aplicar XOR de nuevo con la misma clave):
```bash
chmod +x xor_descifrar.py
python3 xor_descifrar.py
```
```
Texto original: anagrama:amargana
```
![Ejecución del script inverso obteniendo la contraseña](assets/page-14.jpg)
Resultado: `encrypt9` / `anagrama:amargana`
---
encrypt9 (Reto final con cifrado afín modular)
En `encrypt9` encontramos `msg2.enc` y un script `chall_crypto.py`:
```bash
ls
# chall_crypto.py  msg2.enc

cat msg2.enc
# 966772a367ec53998f498553ce99ed724de2f685a3ad7278076e8972ad72ce4972ec677128d8997235729953a3d8852899f66772e267d87253f6ada37bed
```
Intentamos ejecutar el script original, pero falla porque depende de un módulo que no existe en el sistema:
```bash
python3 chall_crypto.py
```
```
Traceback (most recent call last):
  File "/home/encrypt9/chall_crypto.py", line 2, in <module>
    from secretfile import MSG
ModuleNotFoundError: No module named 'secretfile'
```
![Error al ejecutar el script por módulo faltante](assets/page-14.jpg)
Analizando `msg2.enc`, identificamos que el contenido es una cadena hexadecimal que oculta un cifrado afín modular del tipo `c = (m - k) * a mod 256`. Lo descifrramos directamente desde la terminal con Python, sin depender del script roto:
```bash
python3 -c "ct=open('msg2.enc').read().strip(); print(''.join(chr(((b-18)*179)%256) for b in bytes.fromhex(ct)))"
```
```
Lo conseguiste! Aplica ROT5 a tu nombre y escribelo por slack!
```
![Mensaje final descifrado con Python en una línea](assets/page-15.jpg)
---
7. Resumen de credenciales
```
| # | Usuario | Contraseña | Técnica empleada |
|---|---|---|---|
| 1 | `encode1` | `encode1` | Texto plano en `info.txt` |
| 2 | `encode2` | `revers3D` | Texto invertido (`rev`) |
| 3 | `encode3` | `B4se64` | Base64 |
| 4 | `encode4` | `D3sreveR46es4B` | Base64 invertido |
| 5 | `encode5` | `H3xToT3xt` | Hexadecimal → ASCII (`xxd -r -p`) |
| 6 | `encode6` | `ASD3cimalCI` | Decimal/Entero (cryptii.com) |
| 7 | `encode7` | `URL<'#'>Encoding` | URL Encoding (cryptii.com) |
| 8 | `encode8` | `Text2Binary` | Binario → texto (cryptii.com) |
| 9 | `encrypt1` | `encrypt1` | Texto plano en `flag_mid.txt` |
| 10 | `encrypt2` | `CaesarKn0w` | Cifrado César, 17 posiciones |
| 11 | `encrypt3` | `SustituyeME` | Sustitución alfabética |
| 12 | `encrypt4` | `NotSoEasy` | Transposición columnar (clave `TRANSPOSE`) |
| 13 | `encrypt5` | `EncryptITVigenere` | Cifrado Vigenère (clave `Vigenere`) |
| 14 | `encrypt6` | `3DESEncription!` | OpenSSL 3DES (clave `Symmetric`) |
| 15 | `encrypt7` | `AESEncrypt256` | OpenSSL AES-256-CBC (clave `AES256Symmetric`) |
| 16 | `pkencrypt1` | `pkencrypt1` | Texto plano en `flag_mid.txt` |
| 17 | `pkencrypt2` | `Dec0deASPrivate` | RSA directo (`openssl pkeyutl -decrypt`) |
| 18 | `pkencrypt3` | `KeyExchangeEPH` | Cifrado híbrido RSA + AES (clave efímera) |
| 19 | `hashing1` | `hashing1` | Texto plano en `flag_mid.txt` |
| 20 | `hashing2` | `Check1ngMD5` | Hash MD5 → coincide con `contraseña7.txt` |
| 21 | `hashing3` | `Check1ngSHA1` | Hash SHA-1 → coincide con `contraseña4.txt` |
| 22 | `hashing4` | `BDHey23dsfad890bSHDYsm` | Hash SHA-256 → coincide con `contraseña8.txt` |
| 23 | `hashing5` | `BDHasDFHsydnbSHDYsm` | Hash SHA-512 → coincide con `contraseña9.txt` |
| 24 | `hashing6` | `admin123` | Fuerza bruta MD5 con hashcat |
| 25 | `encrypt8` | `-H@rdl3v3l!!` | Texto plano en `credentials.txt` (vía hashing6) |
| 26 | `encrypt9` | `anagrama:amargana` | Ingeniería inversa de `xor.py` |
``
8. Herramientas utilizadas
Herramienta	Uso en el lab
`arp-scan`	Descubrimiento de hosts en la red NAT
`ssh`	Acceso remoto a la máquina víctima
`rev`	Inversión de cadenas de texto
`base64`	Codificación/decodificación Base64
`xxd`	Conversión hexadecimal ↔ ASCII
cryptii.com	Decimal, URL Encoding, Binario, César, Sustitución, Vigenère
`openssl`	Cifrado/descifrado 3DES, AES-256-CBC, RSA (`pkeyutl`)
`hash-identifier`	Identificación del algoritmo de hash
`md5sum` / `sha1sum` / `sha256sum` / `sha512sum`	Cálculo de hashes para comparación
`hashcat`	Ataque de fuerza bruta sobre hash MD5
`python3`	Scripts de cifrado/descifrado XOR e ingeniería inversa
---
📁 Estructura del repositorio
```
.
├── README.md              # Este documento
└── assets/
    ├── page-01.jpg ... page-15.jpg   # Capturas de pantalla del proceso completo
```
