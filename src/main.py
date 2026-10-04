"""Aplicacion principal.

Flujo de arranque:
1. Conecta WiFi o levanta un AP de rescate.
2. Inicializa el sensor ambiental.
3. Arranca un servidor HTTP con dashboard y API.
"""

import config
from http_server import HttpServer
from sensors import EnvironmentSensor
from wifi_manager import connect_or_start_ap


def main():
    network_info = connect_or_start_ap(config)

    sensor = EnvironmentSensor(
        pin=config.DHT_PIN,
        sensor_type=config.DHT_TYPE,
        read_interval_ms=config.READ_INTERVAL_MS,
    )

    server = HttpServer(
        sensor=sensor,
        device_name=config.DEVICE_NAME,
        port=config.HTTP_PORT,
    )

    print("Modo de red:", network_info["mode"])
    print("Abrir: http://{}/".format(network_info["ip"]))
    server.serve_forever()


main()
