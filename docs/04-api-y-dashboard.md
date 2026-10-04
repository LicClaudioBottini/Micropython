# 04 - API y dashboard

El ESP8266 sirve una pagina HTML y tambien endpoints pensados para sistemas externos.

## Dashboard

Ruta:

```text
GET /
```

La pagina consulta periodicamente:

```text
GET /api/estado
```

No usa frameworks ni archivos externos. Todo esta embebido en `http_server.py` para que sea facil copiarlo a la placa.

## API

### Estado completo

```text
GET /api/estado
GET /estado
```

Respuesta de ejemplo:

```json
{
  "ok": true,
  "temperatura": 24,
  "humedad": 52,
  "unidad_temperatura": "C",
  "sensor": "DHT11",
  "uptime_s": 181,
  "lectura_edad_ms": 1200,
  "error": null
}
```

### Temperatura

```text
GET /temperatura
```

Respuesta:

```json
{"ok": true, "temperatura": 24, "unidad": "C"}
```

### Humedad

```text
GET /humedad
```

Respuesta:

```json
{"ok": true, "humedad": 52, "unidad": "%"}
```

### Salud

```text
GET /health
```

Respuesta:

```json
{"ok": true}
```

## Ejemplos de consumo

PowerShell:

```powershell
Invoke-RestMethod http://192.168.1.37/api/estado
```

curl:

```bash
curl http://192.168.1.37/temperatura
```

Python:

```python
import requests

r = requests.get("http://192.168.1.37/api/estado", timeout=5)
print(r.json())
```

## Sobre GET y POST

Este primer proyecto solo necesita lectura, por eso usa `GET`. El servidor ya separa metodo y ruta, asi que se puede extender con `POST`, por ejemplo:

- `POST /led` para prender/apagar un LED.
- `POST /config` para cambiar algun parametro.
- `POST /releer` para forzar lectura.

Para comandos reales conviene agregar algun tipo de token o red aislada. En una LAN domestica puede parecer exagerado, hasta que deja de serlo.
