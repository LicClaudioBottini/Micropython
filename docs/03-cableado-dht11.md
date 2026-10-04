# 03 - Cableado DHT11

El DHT11 mide temperatura y humedad. Es economico, suficiente para aprender y para monitoreo ambiental simple, aunque no es rapido ni de alta precision.

## Regla de lectura

No conviene leer el DHT11 muchas veces por segundo. Este proyecto cachea la medicion y actualiza cada 3 segundos por defecto.

## Opcion A: NodeMCU o Wemos D1 mini

Usaremos `GPIO4`, que en muchas placas aparece como `D2`.

```text
NodeMCU / Wemos              DHT11 modulo 3 pines
----------------             --------------------
3V3             ----------->  VCC / +
GND             ----------->  GND / -
D2 / GPIO4      ----------->  DATA / OUT
```

Si tu DHT11 es un sensor pelado de 4 pines mirando la rejilla de frente:

```text
DHT11 pelado, frente visible

  +-----+
  | ::: |
  +-----+
   1 2 3 4

1 VCC  -> 3V3
2 DATA -> GPIO4
3 NC   -> sin conectar
4 GND  -> GND
```

Agrega una resistencia de 4.7 kOhm a 10 kOhm entre `DATA` y `3V3`, salvo que uses un modulo DHT11 que ya la trae.

```text
3V3 ----+---------------- VCC DHT11
        |
       [10k]
        |
GPIO4 --+---------------- DATA DHT11

GND ---------------------- GND DHT11
```

## Opcion B: modulo ESP-12 suelto

El modulo ESP-12 necesita cableado de arranque ademas del DHT11. Para pruebas iniciales, esta es la configuracion tipica:

```text
ESP-12 / ESP8266MOD

VCC       -> 3.3 V estable
GND       -> GND
EN/CH_PD  -> 3.3 V con pull-up 10k
RST       -> 3.3 V con pull-up 10k
GPIO0     -> 3.3 V con pull-up 10k para arranque normal
GPIO2     -> 3.3 V con pull-up 10k
GPIO15    -> GND con pull-down 10k
TX        -> RX del USB-TTL 3.3 V
RX        -> TX del USB-TTL 3.3 V
GPIO4     -> DATA del DHT11
```

Para flashear firmware, `GPIO0` debe ir a GND durante el reset. Para ejecutar el programa normalmente, `GPIO0` debe quedar alto.

## Pines recomendados

Para sensores digitales simples, preferi:

- `GPIO4`
- `GPIO5`
- `GPIO12`
- `GPIO13`
- `GPIO14`

Evita para empezar:

- `GPIO0`, `GPIO2`, `GPIO15`: participan en el modo de arranque.
- `GPIO1` y `GPIO3`: TX/RX serie.
- `GPIO16`: sirve, pero tiene particularidades y no siempre va bien con todas las librerias.
