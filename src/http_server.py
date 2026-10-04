"""Servidor HTTP minimo para dashboard y API REST.

Esta implementacion evita dependencias externas para entrar comodamente en un
ESP8266. No busca competir con un framework web: solo resuelve rutas simples,
devuelve JSON y sirve una pagina HTML embebida.
"""

import gc
import json
import socket
import time


def _json_response(payload, status="200 OK"):
    body = json.dumps(payload)
    return (
        "HTTP/1.1 {}\r\n"
        "Content-Type: application/json; charset=utf-8\r\n"
        "Cache-Control: no-store\r\n"
        "Connection: close\r\n"
        "Content-Length: {}\r\n"
        "\r\n"
        "{}"
    ).format(status, len(body), body)


def _text_response(text, status="200 OK", content_type="text/plain; charset=utf-8"):
    return (
        "HTTP/1.1 {}\r\n"
        "Content-Type: {}\r\n"
        "Cache-Control: no-store\r\n"
        "Connection: close\r\n"
        "Content-Length: {}\r\n"
        "\r\n"
        "{}"
    ).format(status, content_type, len(text), text)


def _dashboard_html(device_name):
    return """<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{device_name}</title>
  <style>
    :root {{
      color-scheme: light dark;
      --bg: #f4f7f9;
      --panel: #ffffff;
      --text: #172026;
      --muted: #66717a;
      --line: #d9e1e7;
      --accent: #0b7fab;
      --ok: #168a4a;
      --bad: #b42318;
    }}
    @media (prefers-color-scheme: dark) {{
      :root {{
        --bg: #101417;
        --panel: #171d21;
        --text: #edf2f5;
        --muted: #9aa7b0;
        --line: #2a3339;
        --accent: #4db6d7;
      }}
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: system-ui, -apple-system, Segoe UI, sans-serif;
      background: var(--bg);
      color: var(--text);
    }}
    main {{
      width: min(920px, calc(100vw - 32px));
      margin: 0 auto;
      padding: 28px 0;
    }}
    header {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 18px;
    }}
    h1 {{
      margin: 0;
      font-size: clamp(1.4rem, 4vw, 2.1rem);
      letter-spacing: 0;
    }}
    .subtitle {{
      margin-top: 6px;
      color: var(--muted);
      font-size: 0.95rem;
    }}
    .status {{
      min-width: 96px;
      text-align: center;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 8px 10px;
      font-weight: 700;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 14px;
    }}
    .card {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 18px;
      min-height: 150px;
    }}
    .label {{
      color: var(--muted);
      font-size: 0.9rem;
      margin-bottom: 10px;
    }}
    .value {{
      font-size: clamp(2.2rem, 9vw, 4.2rem);
      line-height: 1;
      font-weight: 800;
      letter-spacing: 0;
    }}
    .unit {{
      color: var(--muted);
      font-size: 1rem;
      margin-left: 4px;
    }}
    .details {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px 18px;
      margin-top: 14px;
      color: var(--muted);
      font-size: 0.95rem;
    }}
    code {{
      color: var(--accent);
      overflow-wrap: anywhere;
    }}
    @media (max-width: 640px) {{
      header, .grid, .details {{
        grid-template-columns: 1fr;
      }}
      header {{
        display: block;
      }}
      .status {{
        margin-top: 14px;
        width: 100%;
      }}
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <div>
        <h1>{device_name}</h1>
        <div class="subtitle">Estacion ambiental local ESP8266 + DHT</div>
      </div>
      <div id="status" class="status">...</div>
    </header>

    <section class="grid">
      <article class="card">
        <div class="label">Temperatura</div>
        <div><span id="temp" class="value">--</span><span class="unit">C</span></div>
      </article>
      <article class="card">
        <div class="label">Humedad</div>
        <div><span id="hum" class="value">--</span><span class="unit">%</span></div>
      </article>
    </section>

    <section class="card" style="margin-top:14px">
      <div class="label">API local</div>
      <div class="details">
        <div>Estado: <code>/api/estado</code></div>
        <div>Temperatura: <code>/temperatura</code></div>
        <div>Humedad: <code>/humedad</code></div>
        <div>Ultima lectura: <span id="age">--</span></div>
      </div>
      <p id="error" style="color:var(--bad); margin-bottom:0"></p>
    </section>
  </main>

  <script>
    async function refresh() {{
      const status = document.getElementById("status");
      const error = document.getElementById("error");
      try {{
        const res = await fetch("/api/estado", {{ cache: "no-store" }});
        const data = await res.json();
        document.getElementById("temp").textContent = data.temperatura ?? "--";
        document.getElementById("hum").textContent = data.humedad ?? "--";
        document.getElementById("age").textContent =
          data.lectura_edad_ms === null ? "--" : Math.round(data.lectura_edad_ms / 1000) + " s";
        status.textContent = data.ok ? "OK" : "ERROR";
        status.style.color = data.ok ? "var(--ok)" : "var(--bad)";
        error.textContent = data.error || "";
      }} catch (err) {{
        status.textContent = "SIN RED";
        status.style.color = "var(--bad)";
        error.textContent = err.message;
      }}
    }}
    refresh();
    setInterval(refresh, 3000);
  </script>
</body>
</html>""".format(device_name=device_name)


class HttpServer:
    def __init__(self, sensor, device_name="meteo-esp8266", port=80):
        self.sensor = sensor
        self.device_name = device_name
        self.port = port
        self.started_at_ms = time.ticks_ms()

    def _state(self):
        state = self.sensor.read()
        state["device"] = self.device_name
        state["uptime_s"] = time.ticks_diff(time.ticks_ms(), self.started_at_ms) // 1000
        return state

    def _handle(self, method, path):
        if method == "GET" and path == "/":
            return _text_response(_dashboard_html(self.device_name), content_type="text/html; charset=utf-8")

        if method == "GET" and path in ("/api/estado", "/estado"):
            return _json_response(self._state())

        if method == "GET" and path == "/temperatura":
            state = self._state()
            return _json_response({
                "ok": state["ok"],
                "temperatura": state["temperatura"],
                "unidad": "C",
                "error": state["error"],
            })

        if method == "GET" and path == "/humedad":
            state = self._state()
            return _json_response({
                "ok": state["ok"],
                "humedad": state["humedad"],
                "unidad": "%",
                "error": state["error"],
            })

        if method == "GET" and path == "/health":
            return _json_response({"ok": True})

        if method == "POST" and path == "/api/releer":
            state = self.sensor.read(force=True)
            state["device"] = self.device_name
            return _json_response(state)

        return _json_response({"ok": False, "error": "Ruta no encontrada"}, "404 Not Found")

    def serve_forever(self):
        addr = socket.getaddrinfo("0.0.0.0", self.port)[0][-1]
        server = socket.socket()
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(addr)
        server.listen(3)
        print("Servidor HTTP escuchando en puerto", self.port)

        while True:
            client = None
            try:
                client, remote_addr = server.accept()
                request = client.recv(1024)
                if not request:
                    continue

                # La primera linea HTTP es ASCII; decode() simple es mas portable
                # entre builds de MicroPython que decode(..., errors=...) .
                first_line = request.decode().split("\r\n", 1)[0]
                parts = first_line.split()
                if len(parts) < 2:
                    response = _json_response({"ok": False, "error": "Request invalido"}, "400 Bad Request")
                else:
                    method = parts[0]
                    path = parts[1].split("?", 1)[0]
                    response = self._handle(method, path)

                client.send(response.encode())
            except Exception as exc:
                try:
                    client.send(_json_response({"ok": False, "error": str(exc)}, "500 Internal Server Error").encode())
                except Exception:
                    pass
                print("Error HTTP:", exc)
            finally:
                if client:
                    client.close()
                gc.collect()
