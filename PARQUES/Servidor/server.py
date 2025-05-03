import asyncio
import websockets
import json
import random

MAX_JUGADORES = 4
jugadores_conectados = {}  # websocket: {nombre, color}
colores_disponibles = ["rojo", "azul", "verde", "amarillo"]
partida_en_curso = False
jugadores_ordenados = []
turno_actual = 0
pares_consecutivos = {}  # websocket: int
estado_jugadores = {}  # websocket: {fichas: [estado, estado, estado, estado]}

def casilla_salida_por_color(color):
    salidas = {
        "rojo": 0,
        "verde": 19,
        "amarillo": 38,
        "azul": 57
    }
    return salidas.get(color, 0)

async def manejar_jugador(websocket, path):
    global partida_en_curso, turno_actual

    if len(jugadores_conectados) >= MAX_JUGADORES or partida_en_curso:
        await websocket.send(json.dumps({"tipo": "rechazo", "motivo": "Partida en curso o máximo de jugadores alcanzado"}))
        await websocket.close()
        return

    await websocket.send(json.dumps({"tipo": "solicitar_nombre"}))
    mensaje = await websocket.recv()
    datos = json.loads(mensaje)

    nombre = datos.get("nombre")
    if not nombre:
        await websocket.send(json.dumps({"tipo": "error", "mensaje": "Nombre inválido"}))
        return

    color_asignado = colores_disponibles.pop(0)
    jugadores_conectados[websocket] = {"nombre": nombre, "color": color_asignado}
    await websocket.send(json.dumps({"tipo": "confirmacion", "color": color_asignado}))
    print(f"{nombre} se ha conectado con el color {color_asignado}")

    if len(jugadores_conectados) == MAX_JUGADORES:
        partida_en_curso = True
        await iniciar_partida()

    try:
        while True:
            mensaje = await websocket.recv()
            datos = json.loads(mensaje)

            if datos["tipo"] == "lanzar_dados":
                if websocket != jugadores_ordenados[turno_actual]:
                    await websocket.send(json.dumps({"tipo": "error", "mensaje": "No es tu turno"}))
                    continue

                dado1 = random.randint(1, 6)
                dado2 = random.randint(1, 6)
                es_par = dado1 == dado2

                await websocket.send(json.dumps({
                    "tipo": "resultado_dados",
                    "dado1": dado1,
                    "dado2": dado2,
                    "par": es_par
                }))

                if es_par:
                    pares_consecutivos[websocket] += 1
                    if pares_consecutivos[websocket] == 3:
                        await websocket.send(json.dumps({
                            "tipo": "bonus_sacar_ficha",
                            "mensaje": "Has sacado 3 pares consecutivos. Puedes sacar una ficha del juego."
                        }))
                        pares_consecutivos[websocket] = 0
                    await notificar_turno()
                else:
                    pares_consecutivos[websocket] = 0
                    turno_actual = (turno_actual + 1) % len(jugadores_ordenados)
                    await notificar_turno()

            elif datos["tipo"] == "mover_ficha":
                if websocket != jugadores_ordenados[turno_actual]:
                    await websocket.send(json.dumps({"tipo": "error", "mensaje": "No es tu turno"}))
                    continue

                indice = datos.get("indice_ficha")
                cantidad = datos.get("cantidad")

                if indice is None or cantidad is None:
                    await websocket.send(json.dumps({"tipo": "error", "mensaje": "Datos de movimiento incompletos"}))
                    continue

                ficha = estado_jugadores[websocket]["fichas"][indice]

                if ficha["posicion"] == -1:
                    await websocket.send(json.dumps({
                        "tipo": "error",
                        "mensaje": "La ficha está en la cárcel y no puede moverse así"
                    }))
                    continue

                nueva_pos = ficha["posicion"] + cantidad

                if nueva_pos >= 76:
                    ficha["posicion"] = 100
                    ficha["activa"] = False
                    await websocket.send(json.dumps({"tipo": "ficha_llegada", "indice": indice}))
                else:
                    ficha["posicion"] = nueva_pos
                    await websocket.send(json.dumps({
                        "tipo": "ficha_movida",
                        "indice": indice,
                        "nueva_posicion": nueva_pos
                    }))

                turno_actual = (turno_actual + 1) % len(jugadores_ordenados)
                await notificar_turno()

            elif datos["tipo"] == "sacar_ficha":
                if websocket != jugadores_ordenados[turno_actual]:
                    await websocket.send(json.dumps({"tipo": "error", "mensaje": "No es tu turno"}))
                    continue

                indice = datos.get("indice_ficha")
                ficha = estado_jugadores[websocket]["fichas"][indice]

                if ficha["posicion"] != -1:
                    await websocket.send(json.dumps({"tipo": "error", "mensaje": "La ficha no está en la cárcel"}))
                    continue

                color = jugadores_conectados[websocket]["color"]
                ficha["posicion"] = casilla_salida_por_color(color)
                ficha["activa"] = True

                await websocket.send(json.dumps({
                    "tipo": "ficha_sacada",
                    "indice": indice,
                    "posicion": ficha["posicion"]
                }))

    except websockets.exceptions.ConnectionClosed:
        print(f"{nombre} se ha desconectado.")
        if websocket in jugadores_conectados:
            colores_disponibles.append(jugadores_conectados[websocket]["color"])
            del jugadores_conectados[websocket]
            partida_en_curso = False

async def notificar_turno():
    jugador_ws = jugadores_ordenados[turno_actual]
    await jugador_ws.send(json.dumps({"tipo": "tu_turno"}))

async def iniciar_partida():
    global jugadores_ordenados, turno_actual, pares_consecutivos

    print("¡Iniciando partida!")
    jugadores_ordenados = list(jugadores_conectados.keys())
    random.shuffle(jugadores_ordenados)
    turno_actual = 0
    pares_consecutivos = {ws: 0 for ws in jugadores_ordenados}

    for ws in jugadores_ordenados:
        estado_jugadores[ws] = {
            "fichas": [{"posicion": -1, "activa": False} for _ in range(4)]
        }

    for ws in jugadores_conectados:
        await ws.send(json.dumps({
            "tipo": "iniciar_partida",
            "jugadores": [jugadores_conectados[j]["nombre"] for j in jugadores_ordenados],
            "turno_inicial": jugadores_conectados[jugadores_ordenados[0]]["nombre"]
        }))

    await notificar_turno()

start_server = websockets.serve(manejar_jugador, "localhost", 8765)

async def main():
    print("Servidor iniciado en ws://localhost:8765")
    async with websockets.serve(manejar_jugador, "localhost", 8765):
        await asyncio.Future()  # mantener corriendo

asyncio.run(main())
