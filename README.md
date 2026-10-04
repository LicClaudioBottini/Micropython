# Estacion meteorologica local con ESP8266 y DHT11

Proyecto de iniciacion a MicroPython para armar una estacion ambiental local:

- Lee temperatura y humedad desde un sensor DHT11.
- Conecta el modulo ESP8266 a tu red WiFi.
- Sirve un dashboard web simple desde la propia placa.
- Expone endpoints HTTP para monitoreo externo:
  - `GET /temperatura`
  - `GET /humedad`
  - `GET /api/estado`
  - `GET /estado`

La placa no guarda historial. La idea es que otro sistema consulte la API y almacene los datos, por ejemplo Home Assistant, Grafana, Node-RED, Zabbix, Prometheus con un exporter, o un script propio.

> Nota importante: el modulo de la foto es un `ESP8266MOD` tipo ESP-12, no un ESP32. Este proyecto esta escrito para MicroPython en ESP8266.

## Estructura

```text
.
|-- README.md
|-- docs/
|   |-- 01-preparacion-entorno.md
|   |-- 02-pruebas-wifi-sin-sensor.md
|   |-- 03-cableado-dht11.md
|   |-- 04-api-y-dashboard.md
|   `-- 05-extension-a-mas-sensores.md
`-- src/
    |-- boot.py
    |-- config.py
    |-- main.py
    |-- http_server.py
    |-- sensors.py
    `-- wifi_manager.py
```

## Camino recomendado

1. Segui [Preparacion del entorno](docs/01-preparacion-entorno.md).
2. Copia `src/config.py` a la placa y cambia `WIFI_SSID` / `WIFI_PASSWORD`.
3. Proba conectividad sin sensor con [Pruebas WiFi sin sensor](docs/02-pruebas-wifi-sin-sensor.md).
4. Conecta el DHT11 segun [Cableado DHT11](docs/03-cableado-dht11.md).
5. Copia todos los archivos de `src/` a la placa.
6. Reinicia la placa y entra al dashboard desde un navegador:

```text
http://IP_DE_LA_PLACA/
```

Ejemplos de API:

```text
http://IP_DE_LA_PLACA/temperatura
http://IP_DE_LA_PLACA/humedad
http://IP_DE_LA_PLACA/api/estado
```

## Supuestos de hardware

El proyecto asume:

- ESP8266 con MicroPython.
- Alimentacion estable de 3.3 V.
- DHT11 alimentado a 3.3 V.
- Pin de datos del DHT11 conectado a `GPIO4` por defecto.
- Resistencia pull-up de 4.7 kOhm a 10 kOhm entre DATA y 3.3 V si tu modulo DHT11 no la trae integrada.

Si usas NodeMCU o Wemos D1 mini, `GPIO4` suele estar rotulado como `D2`.

