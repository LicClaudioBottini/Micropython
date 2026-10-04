# 02 - Pruebas WiFi sin sensor

Antes de conectar el DHT11 conviene probar que el ESP8266 se conecta a tu red y sirve HTTP. Asi separamos problemas: primero red, despues sensor.

## 1. Configurar WiFi

Edita `src/config.py` antes de copiarlo a la placa:

```python
WIFI_SSID = "NombreDeTuWiFi"
WIFI_PASSWORD = "ClaveDeTuWiFi"
```

Luego copia estos archivos a la raiz de la placa:

```text
boot.py
config.py
main.py
http_server.py
sensors.py
wifi_manager.py
```

## 2. Arrancar sin sensor

El servidor puede arrancar aunque el DHT11 no este conectado. En ese caso el dashboard muestra error de lectura, pero la red y la API funcionan.

En el REPL deberias ver algo parecido a:

```text
Conectando a WiFi: TuRed
WiFi conectado
IP: 192.168.1.37
Servidor HTTP escuchando en http://192.168.1.37/
```

## 3. Probar desde navegador

Desde una computadora o celular conectado a la misma red:

```text
http://192.168.1.37/
```

Cambia la IP por la que te muestre la placa.

## 4. Probar la API

Desde navegador:

```text
http://192.168.1.37/api/estado
http://192.168.1.37/temperatura
http://192.168.1.37/humedad
```

Desde PowerShell:

```powershell
Invoke-RestMethod http://192.168.1.37/api/estado
```

Si todavia no conectaste el sensor, es normal recibir un JSON con `ok: false`.

## 5. Modo AP de rescate

Si no logra conectarse al WiFi configurado, el proyecto crea una red propia:

```text
SSID: MeteoESP8266-Setup
Clave: configurar123
IP: 192.168.4.1
```

Conectate a esa red y abre:

```text
http://192.168.4.1/
```

Esto no configura credenciales desde web todavia; es un modo de rescate para poder entrar al dashboard y saber que la placa esta viva.
