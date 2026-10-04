"""Lectura de sensores ambientales.

La clase mantiene cache para no exigir al DHT11 mas lecturas de las que soporta.
Esto tambien hace que varias peticiones HTTP seguidas respondan rapido.
"""

import dht
import machine
import time


class EnvironmentSensor:
    def __init__(self, pin, sensor_type="DHT11", read_interval_ms=3000):
        self.pin = pin
        self.sensor_type = sensor_type
        self.read_interval_ms = read_interval_ms
        self._last_read_ms = None
        self._last_ok_ms = None
        self._temperature = None
        self._humidity = None
        self._error = "Sensor sin leer todavia"

        data_pin = machine.Pin(pin)
        if sensor_type.upper() == "DHT22":
            self._sensor = dht.DHT22(data_pin)
        else:
            self._sensor = dht.DHT11(data_pin)

    def read(self, force=False):
        now = time.ticks_ms()

        if (
            not force
            and self._last_read_ms is not None
            and time.ticks_diff(now, self._last_read_ms) < self.read_interval_ms
        ):
            return self.state()

        self._last_read_ms = now

        try:
            self._sensor.measure()
            self._temperature = self._sensor.temperature()
            self._humidity = self._sensor.humidity()
            self._last_ok_ms = now
            self._error = None
        except Exception as exc:
            self._error = "{}: {}".format(type(exc).__name__, exc)

        return self.state()

    def state(self):
        now = time.ticks_ms()
        age = None
        if self._last_ok_ms is not None:
            age = time.ticks_diff(now, self._last_ok_ms)

        return {
            "ok": self._error is None,
            "temperatura": self._temperature,
            "humedad": self._humidity,
            "unidad_temperatura": "C",
            "unidad_humedad": "%",
            "sensor": self.sensor_type,
            "pin": self.pin,
            "lectura_edad_ms": age,
            "error": self._error,
        }
