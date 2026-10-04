"""Conexion WiFi para ESP8266.

El modulo intenta conectarse como estacion a la red configurada. Si no puede,
opcionalmente levanta un Access Point de rescate para poder acceder al servidor.
"""

import network
import time


def connect_or_start_ap(config):
    sta = network.WLAN(network.STA_IF)
    sta.active(True)

    if config.WIFI_SSID and config.WIFI_SSID != "CAMBIAR_WIFI":
        print("Conectando a WiFi:", config.WIFI_SSID)
        sta.connect(config.WIFI_SSID, config.WIFI_PASSWORD)

        start = time.ticks_ms()
        while not sta.isconnected():
            if time.ticks_diff(time.ticks_ms(), start) > 15000:
                break
            time.sleep_ms(250)

        if sta.isconnected():
            ip = sta.ifconfig()[0]
            print("WiFi conectado")
            print("IP:", ip)
            return {
                "mode": "station",
                "ip": ip,
                "ifconfig": sta.ifconfig(),
            }

    print("No se pudo conectar a WiFi")

    if not config.AP_FALLBACK_ENABLED:
        raise RuntimeError("WiFi no conectado y AP fallback deshabilitado")

    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=config.AP_SSID, password=config.AP_PASSWORD, authmode=network.AUTH_WPA_WPA2_PSK)

    # El AP tarda un instante en quedar activo.
    time.sleep_ms(500)
    ip = ap.ifconfig()[0]
    print("Access Point de rescate activo")
    print("SSID:", config.AP_SSID)
    print("IP:", ip)
    return {
        "mode": "access_point",
        "ip": ip,
        "ifconfig": ap.ifconfig(),
    }
