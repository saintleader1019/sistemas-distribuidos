# Backend actualizado con soporte para 4 jugadores con nombre, color único y control de inicio de partida

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from random import randint

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

clients = []
jugadores_conectados = {}  # { websocket: { 'color': 'rojo', 'nombre': 'Juan' } }
colores_disponibles = ["rojo", "amarillo", "azul", "verde"]

juego = {
    "fichas": {},
    "turno": None,
    "nombre_turno": None,
    "dados": {},
    "estado_turno": "esperando_inicio",
    "intentos_carcel": {},
    "valores_disponibles": {}
}

CIRCULAR_PATH_IDS = list(range(68))
SALIDAS = {
    "rojo": 0,
    "amarillo": 17,
    "azul": 34,
    "verde": 51
}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive_json()

    if data.get("accion") != "registro" or "nombre" not in data:
        await websocket.close()
        return

    if len(jugadores_conectados) >= 4 or not colores_disponibles:
        await websocket.send_json({"accion": "rechazado", "motivo": "Juego lleno"})
        await websocket.close()
        return

    color_asignado = colores_disponibles.pop(0)
    jugadores_conectados[websocket] = {"color": color_asignado, "nombre": data["nombre"]}
    clients.append(websocket)

    print(f"[CONECTADO] {data['nombre']} ({color_asignado})")

    juego["fichas"].setdefault(color_asignado, [ {"id": i, "pos": 68+i+(4*len(jugadores_conectados)-4)} for i in range(4) ])
    juego["intentos_carcel"].setdefault(color_asignado, 0)
    juego["valores_disponibles"].setdefault(color_asignado, [])

    await websocket.send_json({"accion": "esperando_inicio", "color": color_asignado})

    if len(jugadores_conectados) == 1:
        await websocket.send_json({"accion": "mostrar_boton_inicio"})

    try:
        while True:
            data = await websocket.receive_json()
            print(f"[RECEIVED] Acción: {data.get('accion')} | Datos: {data}")
            accion = data.get("accion")
            jugador = jugadores_conectados[websocket]["color"]

            if accion == "iniciar_partida":
                juego["turno"] = jugador
                juego["nombre_turno"] = jugadores_conectados[websocket]["nombre"]
                juego["estado_turno"] = "esperando_lanzamiento"
                for client, datos in jugadores_conectados.items():
                    await client.send_json({
                        "accion": "estado_inicial",
                        "turno": juego["turno"],
                        "nombre_turno": juego["nombre_turno"]
                    })
                print(f"[INICIO] Comienza el turno de {juego['nombre_turno']} ({juego['turno']})")

            elif accion == "lanzar_dados":
                if jugador != juego["turno"] or juego["estado_turno"] != "esperando_lanzamiento":
                    await websocket.send_json({"accion": "rechazado", "motivo": "Turno inválido"})
                    continue

                dado1, dado2 = randint(1, 6), randint(1, 6)
                juego["dados"][jugador] = (dado1, dado2)
                juego["valores_disponibles"][jugador] = [dado1, dado2, dado1 + dado2]
                print(f"[DADOS] {jugador} lanzó: {dado1}, {dado2} → opciones: {juego['valores_disponibles'][jugador]}")

                for client in jugadores_conectados:
                    await client.send_json({
                        "accion": "resultado_dados",
                        "jugador": jugador,
                        "dado1": dado1,
                        "dado2": dado2,
                        "valores": juego["valores_disponibles"][jugador]
                    })

                fichas = juego["fichas"][jugador]
                en_carcel = all(f["pos"] not in CIRCULAR_PATH_IDS for f in fichas)

                if en_carcel and dado1 != dado2:
                    juego["intentos_carcel"][jugador] += 1
                    if juego["intentos_carcel"][jugador] >= 3:
                        await pasar_turno(jugador)
                    else:
                        juego["estado_turno"] = "esperando_lanzamiento"
                        await websocket.send_json({
                            "accion": "rechazado",
                            "motivo": f"Necesitas pares para salir (Intento {juego['intentos_carcel'][jugador]}/3)",
                            "reintentar": True
                        })
                else:
                    juego["estado_turno"] = "esperando_movimiento"

            elif accion == "mover":
                ficha_id = data.get("fichaId")
                valor = data.get("valor")
                if jugador != juego["turno"] or juego["estado_turno"] != "esperando_movimiento":
                    await websocket.send_json({"accion": "rechazado", "motivo": "No puedes mover ahora"})
                    continue

                if valor not in juego["valores_disponibles"][jugador]:
                    await websocket.send_json({"accion": "rechazado", "motivo": "Valor no válido"})
                    continue

                ficha = next((f for f in juego["fichas"][jugador] if f["id"] == ficha_id), None)
                if not ficha:
                    await websocket.send_json({"accion": "rechazado", "motivo": "Ficha no encontrada"})
                    continue

                dado1, dado2 = juego["dados"][jugador]
                suma = dado1 + dado2
                if ficha["pos"] not in CIRCULAR_PATH_IDS:
                    if dado1 == dado2:
                        ficha["pos"] = SALIDAS[jugador]
                        juego["intentos_carcel"][jugador] = 0
                    else:
                        await websocket.send_json({"accion": "rechazado", "motivo": "Ficha en cárcel sin pares"})
                        continue
                else:
                    ficha["pos"] = (ficha["pos"] + valor) % 68

                if valor == suma:
                    juego["valores_disponibles"][jugador] = []
                elif valor == dado1:
                    juego["valores_disponibles"][jugador] = [v for v in juego["valores_disponibles"][jugador] if v != dado2 and v != suma]
                elif valor == dado2:
                    juego["valores_disponibles"][jugador] = [v for v in juego["valores_disponibles"][jugador] if v != dado1 and v != suma]

                print(f"[MOVER] {jugador} movió ficha {ficha_id} a casilla {ficha['pos']} con valor {valor}")
                print(f"[MOVIMIENTO] Valores restantes para {jugador}: {juego['valores_disponibles'][jugador]}")

                if not juego["valores_disponibles"][jugador]:
                    await pasar_turno(jugador)

                for client in jugadores_conectados:
                    await client.send_json({
                        "accion": "mover",
                        "jugador": jugador,
                        "fichaId": ficha_id,
                        "nuevaCasillaId": ficha["pos"],
                        "turno": juego["turno"],
                        "restantes": juego["valores_disponibles"][jugador]
                    })

    except WebSocketDisconnect:
        if websocket in jugadores_conectados:
            print(f"[DESCONECTADO] {jugadores_conectados[websocket]['nombre']} ({jugadores_conectados[websocket]['color']})")
            colores_disponibles.append(jugadores_conectados[websocket]["color"])
            clients.remove(websocket)
            jugadores_conectados.pop(websocket)

async def pasar_turno(jugador):
    orden = ["rojo", "amarillo", "azul", "verde"]
    idx = orden.index(jugador)
    for i in range(1, 5):
        siguiente = orden[(idx + i) % 4]
        if siguiente in [j["color"] for j in jugadores_conectados.values()]:
            juego["turno"] = siguiente
            juego["estado_turno"] = "esperando_lanzamiento"
            juego["dados"].pop(jugador, None)
            juego["valores_disponibles"][jugador] = []
            juego["nombre_turno"] = next(j["nombre"] for j in jugadores_conectados.values() if j["color"] == siguiente)
            print(f"[TURNO] Cambio de turno → ahora juega: {juego['nombre_turno']} ({juego['turno']})")
            for client in jugadores_conectados:
                await client.send_json({
                    "accion": "pasar_turno",
                    "jugador": jugador,
                    "turno": siguiente,
                    "nombre_turno": juego["nombre_turno"]
                })
            break

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
