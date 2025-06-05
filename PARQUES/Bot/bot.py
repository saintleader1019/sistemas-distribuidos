# Bot actualizado para integrarse con el backend actual de Parques

import asyncio
import websockets
import json
import random

BOT_NOMBRE = "Santiago"
SERVER_URL = "ws://localhost:8000/ws"

fichas_bot = [{"posicion": -1, "id": i} for i in range(4)]
mi_color = None
valores_disponibles = []
dado1 = dado2 = 0

async def jugar():
    global mi_color, valores_disponibles, dado1, dado2
    async with websockets.connect(SERVER_URL) as ws:
        await ws.send(json.dumps({"accion": "registro", "nombre": BOT_NOMBRE}))

        while True:
            mensaje = await ws.recv()
            data = json.loads(mensaje)
            print(f"<- {data}")

            accion = data.get("accion")

            if accion == "esperando_inicio":
                mi_color = data["color"]

            elif accion == "mostrar_boton_inicio":
                await asyncio.sleep(1)
                await ws.send(json.dumps({"accion": "iniciar_partida"}))

            elif accion == "estado_inicial":
                pass  # Se puede usar para reiniciar variables si es necesario

            elif accion == "resultado_dados" and data.get("jugador") == mi_color:
                dado1 = data.get("dado1")
                dado2 = data.get("dado2")
                valores_disponibles = data.get("valores", [])

                await asyncio.sleep(1)
                # Intentar mover una ficha desde la cárcel con dobles
                if dado1 == dado2:
                    for ficha in fichas_bot:
                        if ficha["posicion"] < 0:
                            await ws.send(json.dumps({
                                "accion": "mover",
                                "jugador": mi_color,
                                "fichaId": ficha["id"],
                                "valor": dado1 + dado2
                            }))
                            break
                else:
                    # Intentar mover una ficha que ya esté en el camino
                    for ficha in fichas_bot:
                        if ficha["posicion"] in range(0, 68):
                            await ws.send(json.dumps({
                                "accion": "mover",
                                "jugador": mi_color,
                                "fichaId": ficha["id"],
                                "valor": valores_disponibles[-1]  # intenta mover la suma si está
                            }))
                            break

            elif accion == "mover":
                if data["jugador"] == mi_color:
                    idx = data["fichaId"]
                    nueva = data["nuevaCasillaId"]
                    for ficha in fichas_bot:
                        if ficha["id"] == idx:
                            ficha["posicion"] = nueva
                            break
                    valores_disponibles = data.get("restantes", [])

                    await asyncio.sleep(1)
                    if valores_disponibles:
                        for ficha in fichas_bot:
                            if ficha["posicion"] in range(0, 68):
                                await ws.send(json.dumps({
                                    "accion": "mover",
                                    "jugador": mi_color,
                                    "fichaId": ficha["id"],
                                    "valor": valores_disponibles[-1]
                                }))
                                break

            elif accion == "rechazado" and data.get("reintentar"):
                await asyncio.sleep(1)
                await ws.send(json.dumps({"accion": "lanzar_dados", "jugador": mi_color}))

            elif accion == "pasar_turno":
                if data.get("turno") == mi_color:
                    await asyncio.sleep(1)
                    await ws.send(json.dumps({"accion": "lanzar_dados", "jugador": mi_color}))

if __name__ == "__main__":
    asyncio.run(jugar())
