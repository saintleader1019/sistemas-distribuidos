# main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from random import randint

app = FastAPI()

# Permitir acceso desde cualquier origen (para el frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

clients = []

# Estado del juego con múltiples fichas por jugador
game_state = {
    "fichas": {
        "rojo": [ {"id": 0, "pos": 68}, {"id": 1, "pos": 69}, {"id": 2, "pos": 70}, {"id": 3, "pos": 71} ],
        "amarillo": [ {"id": 0, "pos": 72}, {"id": 1, "pos": 73}, {"id": 2, "pos": 74}, {"id": 3, "pos": 75} ],
        "azul": [ {"id": 0, "pos": 76}, {"id": 1, "pos": 77}, {"id": 2, "pos": 78}, {"id": 3, "pos": 79} ],
        "verde": [ {"id": 0, "pos": 80}, {"id": 1, "pos": 81}, {"id": 2, "pos": 82}, {"id": 3, "pos": 83} ]
    },
    "turno": "rojo"
}

# Camino circular (casillas 0 a 67)
CIRCULAR_PATH_IDS = list(range(68))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)

    await websocket.send_json({
        "accion": "estado_inicial",
        "turno": game_state["turno"]
    })

    try:
        while True:
            data = await websocket.receive_json()
            accion = data.get("accion")

            if accion == "mover":
                jugador = data.get("jugador")
                ficha_id = data.get("fichaId")

                if jugador != game_state["turno"]:
                    await websocket.send_json({
                        "accion": "rechazado",
                        "motivo": "No es tu turno",
                        "jugador": jugador,
                        "turno": game_state["turno"]
                    })
                    continue

                fichas_jugador = game_state["fichas"].get(jugador, [])
                ficha = next((f for f in fichas_jugador if f["id"] == ficha_id), None)

                if not ficha:
                    await websocket.send_json({
                        "accion": "rechazado",
                        "motivo": "Ficha no encontrada",
                        "jugador": jugador,
                        "turno": game_state["turno"]
                    })
                    continue

                # Lanzar dado simulado
                dado = randint(1, 6)

                if ficha["pos"] not in CIRCULAR_PATH_IDS:
                    if dado == 5:
                        # Buscar la casilla de salida del jugador
                        salida = {
                            "rojo": 0,
                            "amarillo": 17,
                            "azul": 34,
                            "verde": 51
                        }[jugador]
                        ficha["pos"] = salida

                        # Avanzar turno
                        orden = ["rojo", "amarillo", "azul", "verde"]
                        idx = orden.index(jugador)
                        game_state["turno"] = orden[(idx + 1) % 4]

                        for client in clients:
                            await client.send_json({
                                "accion": "mover",
                                "jugador": jugador,
                                "fichaId": ficha_id,
                                "nuevaCasillaId": salida,
                                "turno": game_state["turno"]
                            })
                    else:
                        await websocket.send_json({
                            "accion": "rechazado",
                            "motivo": f"La ficha está en la cárcel y necesitas un 5 (sacaste {dado})",
                            "jugador": jugador,
                            "turno": game_state["turno"]
                        })
                    continue


                # Mover 3 posiciones como ejemplo
                nueva_pos = (ficha["pos"] + 3) % 68
                ficha["pos"] = nueva_pos

                # Avanzar turno
                orden = ["rojo", "amarillo", "azul", "verde"]
                idx = orden.index(jugador)
                game_state["turno"] = orden[(idx + 1) % 4]

                for client in clients:
                    await client.send_json({
                        "accion": "mover",
                        "jugador": jugador,
                        "fichaId": ficha_id,
                        "nuevaCasillaId": nueva_pos,
                        "turno": game_state["turno"]
                    })

    except WebSocketDisconnect:
        clients.remove(websocket)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
