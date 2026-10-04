"""Configuracion local del proyecto.

Copia este archivo a la raiz del ESP8266 y cambia las credenciales WiFi.
No subas claves reales a repositorios publicos.
"""

DEVICE_NAME = "meteo-esp8266"

WIFI_SSID = "CAMBIAR_WIFI"
WIFI_PASSWORD = "CAMBIAR_CLAVE"

# Si falla la conexion WiFi, se crea este Access Point de rescate.
AP_FALLBACK_ENABLED = True
AP_SSID = "MeteoESP8266-Setup"
AP_PASSWORD = "configurar123"

# DHT11 en GPIO4. En NodeMCU/Wemos suele estar rotulado como D2.
DHT_PIN = 4
DHT_TYPE = "DHT11"

# El DHT11 no debe leerse demasiado seguido.
READ_INTERVAL_MS = 3000

# HTTP
HTTP_PORT = 80
