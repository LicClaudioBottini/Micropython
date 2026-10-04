"""Arranque temprano del ESP8266.

Mantenemos boot.py pequeño: solo ajustes seguros antes de ejecutar main.py.
"""

import gc

gc.collect()
