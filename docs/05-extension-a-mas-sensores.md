# 05 - Extension a mas sensores

La idea del proyecto es que DHT11 sea el primer sensor, no el ultimo. La separacion principal es:

- `sensors.py`: sabe leer sensores y entregar un estado normalizado.
- `http_server.py`: sabe responder HTTP, pero no conoce detalles electricos.
- `wifi_manager.py`: sabe conectar la red.
- `main.py`: arma todo y arranca.

## Formato interno recomendado

Para agregar sensores, conviene que cada lectura termine convertida a un diccionario simple:

```python
{
    "ok": True,
    "temperatura": 24,
    "humedad": 52,
    "presion": 1012,
    "luz": 380,
    "error": None,
}
```

Asi el dashboard y la API pueden crecer sin mezclar drivers con presentacion.

## Sensores candidatos

- BMP280/BME280: presion, temperatura, humedad segun modelo.
- BH1750: luz ambiente por I2C.
- MQ-135: calidad de aire aproximada por ADC, requiere calibracion seria.
- DS18B20: temperatura con cable largo y buena estabilidad.
- Sensor de lluvia o humedad de suelo: usar con cuidado, muchos modelos baratos se corroen.

## Recomendacion de arquitectura

Para instalacion permanente:

- IP fija o reserva DHCP en el router.
- Caja ventilada, sin sol directo.
- Fuente 3.3 V estable.
- Consultas externas cada 10 a 60 segundos, no cada segundo.
- Historial fuera del ESP8266.

El ESP8266 deberia hacer bien una cosa: medir y publicar el estado actual. El almacenamiento, graficos y alarmas pertenecen a otro equipo.
