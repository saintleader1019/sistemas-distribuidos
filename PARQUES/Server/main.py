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

juego = {
    "fichas": {
        "rojo": [ {"id": i, "pos": 68+i} for i in range(4) ],
        "amarillo": [ {"id": i, "pos": 72+i} for i in range(4) ],
        "azul": [ {"id": i, "pos": 76+i} for i in range(4) ],
        "verde": [ {"id": i, "pos": 80+i} for i in range(4) ]
    },
    "turno": "rojo",
    "dados": {},
    "estado_turno": "esperando_lanzamiento",
    "intentos_carcel": {"rojo": 0, "amarillo": 0, "azul": 0, "verde": 0},
    "valores_disponibles": {"rojo": [], "amarillo": [], "azul": [], "verde": []}
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
    clients.append(websocket)

    await websocket.send_json({
        "accion": "estado_inicial",
        "turno": juego["turno"]
    })

    try:
        while True:
            data = await websocket.receive_json()
            accion = data.get("accion")

            if accion == "lanzar_dados":
                jugador = data.get("jugador")
                if jugador != juego["turno"]:
                    await websocket.send_json({
                        "accion": "rechazado",
                        "motivo": "No es tu turno",
                        "jugador": jugador
                    })
                    continue

                if juego["estado_turno"] != "esperando_lanzamiento":
                    await websocket.send_json({
                        "accion": "rechazado",
                        "motivo": "Ya lanzaste los dados",
                        "jugador": jugador
                    })
                    continue

                dado1 = randint(1, 6)
                dado2 = randint(1, 6)
                juego["dados"][jugador] = (dado1, dado2)
                juego["valores_disponibles"][jugador] = [dado1, dado2, dado1 + dado2]

                for client in clients:
                    await client.send_json({
                        "accion": "resultado_dados",
                        "jugador": jugador,
                        "dado1": dado1,
                        "dado2": dado2,
                        "valores": juego["valores_disponibles"][jugador]
                    })

                fichas = juego["fichas"][jugador]
                en_carcel = all(f["pos"] not in CIRCULAR_PATH_IDS for f in fichas)

                if en_carcel:
                    if dado1 == dado2:
                        juego["estado_turno"] = "esperando_movimiento"
                        juego["intentos_carcel"][jugador] = 0
                    else:
                        juego["intentos_carcel"][jugador] += 1
                        intentos = juego["intentos_carcel"][jugador]
                        if intentos >= 3:
                            orden = ["rojo", "amarillo", "azul", "verde"]
                            idx = orden.index(jugador)
                            juego["turno"] = orden[(idx + 1) % 4]
                            juego["dados"].pop(jugador, None)
                            juego["valores_disponibles"][jugador] = []
                            juego["estado_turno"] = "esperando_lanzamiento"
                            juego["intentos_carcel"][jugador] = 0
                            for client in clients:
                                await client.send_json({
                                    "accion": "pasar_turno",
                                    "jugador": jugador,
                                    "motivo": "No pudo salir de la cárcel en 3 intentos",
                                    "turno": juego["turno"]
                                })
                            continue
                        else:
                            juego["estado_turno"] = "esperando_lanzamiento"
                            for client in clients:
                                await client.send_json({
                                    "accion": "rechazado",
                                    "motivo": f"Necesitas pares para salir de la cárcel (Intento {intentos}/3)",
                                    "jugador": jugador,
                                    "reintentar": True
                                })
                            continue
                else:
                    juego["estado_turno"] = "esperando_movimiento"

            elif accion == "mover":
                jugador = data.get("jugador")
                ficha_id = data.get("fichaId")
                valor = data.get("valor")

                print(f"[MOVER] Jugador: {jugador}, Ficha ID: {ficha_id}, Valor usado: {valor}")
                print(f"[MOVER] Valores disponibles antes: {juego['valores_disponibles'][jugador]}")

                if jugador != juego["turno"]:
                    await websocket.send_json({
                        "accion": "rechazado",
                        "motivo": "No es tu turno",
                        "jugador": jugador
                    })
                    continue

                if juego["estado_turno"] != "esperando_movimiento":
                    await websocket.send_json({
                        "accion": "rechazado",
                        "motivo": "Debes lanzar los dados primero",
                        "jugador": jugador
                    })
                    continue

                if valor not in juego["valores_disponibles"][jugador]:
                    await websocket.send_json({
                        "accion": "rechazado",
                        "motivo": f"El valor {valor} no está disponible para mover",
                        "jugador": jugador
                    })
                    continue

                ficha = next((f for f in juego["fichas"][jugador] if f["id"] == ficha_id), None)
                if not ficha:
                    await websocket.send_json({
                        "accion": "rechazado",
                        "motivo": "Ficha no encontrada",
                        "jugador": jugador
                    })
                    continue

                if ficha["pos"] not in CIRCULAR_PATH_IDS:
                    if valor == (juego["dados"][jugador][0] + juego["dados"][jugador][1]):
                        ficha["pos"] = SALIDAS[jugador]
                        juego["intentos_carcel"][jugador] = 0
                    else:
                        await websocket.send_json({
                            "accion": "rechazado",
                            "motivo": "Ficha en cárcel y valor no corresponde a pares",
                            "jugador": jugador
                        })
                        continue
                else:
                    ficha["pos"] = (ficha["pos"] + valor) % 68

                nueva_pos = ficha["pos"]
                juego["valores_disponibles"][jugador].remove(valor)

                print(f"[MOVER] Nueva posición ficha: {nueva_pos}")
                print(f"[MOVER] Valores disponibles después: {juego['valores_disponibles'][jugador]}")

                if not juego["valores_disponibles"][jugador]:
                    orden = ["rojo", "amarillo", "azul", "verde"]
                    idx = orden.index(jugador)
                    juego["turno"] = orden[(idx + 1) % 4]
                    juego["dados"].pop(jugador, None)
                    juego["estado_turno"] = "esperando_lanzamiento"
                    print(f"[TURNO] Se pasa el turno a: {juego['turno']}")

                for client in clients:
                    await client.send_json({
                        "accion": "mover",
                        "jugador": jugador,
                        "fichaId": ficha_id,
                        "nuevaCasillaId": nueva_pos,
                        "turno": juego["turno"],
                        "restantes": juego["valores_disponibles"][jugador]
                    })

    except WebSocketDisconnect:
        if websocket in clients:
            clients.remove(websocket)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
