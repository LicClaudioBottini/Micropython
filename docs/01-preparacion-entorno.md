# 01 - Preparacion del entorno

Este primer paso deja tu computadora hablando con el ESP8266. La meta es llegar a un `Hola mundo` en el REPL y confirmar que MicroPython esta corriendo.

## 1. Identificar la placa

La foto muestra un modulo `ESP8266MOD`, comunmente llamado ESP-12E/ESP-12F segun la variante. Hay dos situaciones posibles:

- **Placa de desarrollo**, por ejemplo NodeMCU o Wemos D1 mini: trae USB, regulador de 3.3 V y circuito de arranque. Es la opcion mas amigable.
- **Modulo ESP-12 suelto**: necesita fuente de 3.3 V, conversor USB-TTL a 3.3 V y resistencias de arranque. No se conecta directo a USB ni a 5 V.

## 2. Instalar Thonny

1. Descarga Thonny desde `https://thonny.org/`.
2. Abre Thonny.
3. En `Tools > Options > Interpreter` selecciona:
   - Interpreter: `MicroPython (ESP8266)`
   - Port: el puerto serie de tu placa.

Si no aparece el puerto, instala el driver USB correspondiente. Muchos NodeMCU usan CH340 o CP2102.

## 3. Flashear MicroPython

Desde Thonny suele ser lo mas simple:

1. `Tools > Options > Interpreter`.
2. Click en `Install or update MicroPython`.
3. Target: `ESP8266`.
4. Elige el puerto.
5. Instala el firmware estable mas reciente para ESP8266.

Alternativa por consola con `esptool`:

```powershell
python -m pip install esptool
python -m esptool --port COMx erase_flash
python -m esptool --port COMx --baud 460800 write_flash --flash_size=detect 0 esp8266-xxxx.bin
```

Cambia `COMx` por tu puerto real y `esp8266-xxxx.bin` por el firmware descargado.

## 4. Primer REPL

En Thonny, abre la consola inferior y prueba:

```python
print("Hola mundo desde MicroPython")
```

Luego:

```python
import machine
machine.freq()
```

Si responde un numero como `80000000` o `160000000`, ya estas dentro de la placa.

## 5. Primer archivo `main.py`

Antes de cargar el proyecto completo, proba un archivo minimo:

```python
print("Arranque correcto")
```

Guardalo en la placa como `main.py` y reinicia. Si el mensaje aparece en la consola, ya tenes el ciclo basico de trabajo:

1. Editar.
2. Guardar en la placa.
3. Reiniciar.
4. Mirar la salida por REPL.

## Cuidado electrico importante

El ESP8266 trabaja a 3.3 V. Sus pines no son tolerantes a 5 V. Una fuente debil o ruidosa causa reinicios, desconexiones WiFi y errores raros.

Para pruebas con placa NodeMCU/Wemos, el USB suele alcanzar. Para modulo ESP-12 suelto, usa un regulador de 3.3 V capaz de entregar picos de al menos 500 mA.
