# Ejercicio de Hashes y Firmas

Repositorio para el laboratorio de hashes, verificacion de integridad y firmas digitales del curso **Cifrado de Informacion**.

La solucion se organizo en scripts pequenos para que cada parte del ejercicio se pueda ejecutar y explicar por separado.

## Objetivo

Este proyecto cubre los siguientes temas:

- comparacion de funciones hash
- consulta de contrasenas expuestas con HIBP
- generacion de manifiestos SHA-256
- verificacion de integridad de archivos
- generacion de claves RSA
- firma y verificacion de manifiestos

## Prompt utilizado

Si se quiere dejar constancia del apoyo recibido, un prompt transparente para este proyecto seria el siguiente:

```text
Necesito ayuda con mi ejercicio de hashes y firmas. Quiero revisar que los scripts queden sencillos, claros y alineados con el enunciado, y tambien necesito mejorar el README con instrucciones de ejecucion, ejemplos y una descripcion breve de cada parte del laboratorio.
```

## Estructura del proyecto

```text
Ejercicio_Hashes_Firmas/
|-- README.md
|-- requirements.txt
|-- .gitignore
|-- explorar_hashes.py
|-- consultar_hibp.py
|-- generar_manifiesto.py
|-- verificar_paquete.py
|-- generar_claves_rsa.py
|-- firmar_manifiesto.py
|-- verificar_firma.py
`-- tests/
    `-- test_pending.py
```

## Requisitos

- Python 3.10 o superior
- `pip`
- conexion a internet para `consultar_hibp.py`

## Instalacion

Desde la carpeta raiz del proyecto:

```bash
py -3 -m pip install -r requirements.txt
```

Dependencias:

- `argon2-cffi`
- `pycryptodome`
- `pytest`

## Como ejecutar

Todos los scripts se ejecutan desde la carpeta raiz del proyecto.

### Comando base

```bash
py -3 nombre_del_script.py
```

### Orden sugerido

1. `py -3 explorar_hashes.py`
2. `py -3 consultar_hibp.py`
3. `py -3 generar_manifiesto.py`
4. `py -3 verificar_paquete.py`
5. `py -3 generar_claves_rsa.py`
6. `py -3 firmar_manifiesto.py`
7. `py -3 verificar_firma.py`

### Scripts disponibles

| Script | Que hace |
|---|---|
| `explorar_hashes.py` | Calcula MD5, SHA-1, SHA-256 y SHA3-256 para `MediSoft-v2.1.0` y `medisoft-v2.1.0`, y cuenta cuantos bits cambian en SHA-256. |
| `consultar_hibp.py` | Consulta cuantas veces aparecen en HIBP las contrasenas `admin`, `123456`, `hospital` y `medisoft2024`. |
| `generar_manifiesto.py` | Genera `SHA256SUMS.txt` con los hashes SHA-256 de al menos 5 archivos indicados por ruta. |
| `verificar_paquete.py` | Recalcula los hashes del manifiesto y reporta que archivos estan correctos o alterados. |
| `generar_claves_rsa.py` | Genera `medisoft_priv.pem` y `medisoft_pub.pem`. |
| `firmar_manifiesto.py` | Firma `SHA256SUMS.txt` y guarda la firma en `SHA256SUMS.sig`. |
| `verificar_firma.py` | Verifica la firma digital usando `medisoft_pub.pem`. |

### Ejemplos de ejecucion

Comparar hashes:

```bash
py -3 explorar_hashes.py
```

Generar manifiesto indicando al menos 5 archivos:

```bash
py -3 generar_manifiesto.py archivo1.txt archivo2.txt archivo3.txt archivo4.txt archivo5.txt
```

Firmar y verificar el manifiesto:

```bash
py -3 generar_claves_rsa.py
py -3 firmar_manifiesto.py
py -3 verificar_firma.py
```

## Notas de implementacion

- El codigo se mantuvo sencillo y directo para que sea facil de leer y explicar en clase.
- `consultar_hibp.py` imprime el SHA-256 de cada contrasena, pero la consulta al endpoint `range` usa SHA-1 porque asi funciona la API de Pwned Passwords.

## Ejecutar pruebas

Para correr las pruebas:

```bash
py -3 -m pytest
```

## Estado actual

Los scripts ya estan implementados y siguen un enfoque simple, sin agregar capas innecesarias para el laboratorio.

## Respuestas a las preguntas de analisis

### Problema 1 — Comparacion de algoritmos

**¿Cuantos bits cambiaron entre los dos hashes SHA-256? ¿Que propiedad demuestra esto?**

Al calcular el XOR bit a bit entre los hashes SHA-256 de `MediSoft-v2.1.0` y `medisoft-v2.1.0`
(diferencia de solo un caracter en mayuscula), se obtienen **120 bits distintos** de un total de 256.
Esto demuestra el **efecto avalancha**: un cambio minimo en la entrada (un solo bit en la 'M' vs 'm')
produce una salida completamente diferente, con aproximadamente la mitad de los bits alterados.
Esta propiedad es fundamental para que las funciones hash sirvan como huellas digitales confiables:
dos archivos casi identicos deben tener hashes completamente distintos.

**¿Por que MD5 es inseguro para integridad de archivos?**

MD5 produce un digest de solo **128 bits**, lo que lo hace vulnerable por dos razones:

1. **Espacio de salida reducido:** con 2^128 posibles hashes, un atacante puede encontrar colisiones
   (dos entradas distintas con el mismo hash) con recursos computacionales modernos. Se han
   demostrado colisiones practicas contra MD5 desde 2004, lo que significa que es posible fabricar
   un archivo malicioso con el mismo hash que el original.

2. **Ataques de preimagen facilitados:** el espacio de busqueda es 2^128 veces menor que en
   SHA-256, reduciendo el costo de fuerza bruta.

SHA-256 usa 256 bits (el doble), lo que eleva el costo de colision a 2^128 operaciones, considerado
computacionalmente inviable con la tecnologia actual.

---

### Problema 5 — Verificacion de Autenticidad

**¿Por que la firma sigue siendo valida cuando se modifica un byte de un archivo de datos?**

La firma digital en `SHA256SUMS.sig` protege el contenido del archivo **`SHA256SUMS.txt`**,
no los archivos del paquete directamente. Cuando se modifica un byte en un archivo de datos
(por ejemplo, `config.txt`), el manifiesto `SHA256SUMS.txt` no cambia: sigue conteniendo el hash
SHA-256 original de ese archivo. Por lo tanto, la firma sobre el manifiesto sigue siendo valida,
ya que el texto firmado no fue alterado.

**¿Que sucede al ejecutar `verificar_paquete.py`?**

`verificar_paquete.py` recalcula el SHA-256 de cada archivo y lo compara contra el hash registrado
en `SHA256SUMS.txt`. Al haber modificado un byte en el archivo de datos, el hash recalculado
ya no coincide con el almacenado en el manifiesto, por lo que el verificador reporta ese archivo
como `ALTERADO`. Este es precisamente el rol de cada capa:

- La **firma digital** garantiza que el manifiesto proviene de MediSoft y no fue reemplazado.
- El **manifiesto de hashes** garantiza que cada archivo del paquete no fue modificado en transito.

Ambas capas son necesarias: sin la firma, un atacante podria reemplazar tanto el paquete como el
manifiesto; sin el manifiesto, la firma no detectaria cambios en archivos individuales.

---

## Documento de referencia

El enunciado original esta en:

```text
Ejercicio Hashes_Firmas.pdf
```
