import asyncio
import websockets
import json
import random

BOT_NOMBRE = "BotParques"
SERVER_URL = "ws://localhost:8000/ws"

fichas_bot = [{"posicion": -1, "activa": False} for _ in range(4)]

async def jugar():
    async with websockets.connect(SERVER_URL) as ws:
        msg = await ws.recv()
        data = json.loads(msg)
        if data.get("tipo") == "solicitar_nombre":
            await ws.send(json.dumps({"nombre": BOT_NOMBRE}))

        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            print(f"<- {data}")

            tipo = data.get("tipo")

            if tipo == "tu_turno":
                await asyncio.sleep(1)
                await ws.send(json.dumps({"tipo": "lanzar_dados"}))

            elif tipo == "resultado_dados":
                dado1 = data.get("dado1")
                dado2 = data.get("dado2")
                suma = dado1 + dado2
                par = data.get("par")
                await asyncio.sleep(1)

                if par:
                    for i, f in enumerate(fichas_bot):
                        if f["posicion"] == -1:
                            await ws.send(json.dumps({"tipo": "sacar_ficha", "indice_ficha": i}))
                            await asyncio.sleep(0.5)

                else:
                    for i, f in enumerate(fichas_bot):
                        if f["posicion"] != -1 and f["posicion"] < 100:
                            await ws.send(json.dumps({"tipo": "mover_ficha", "indice_ficha": i, "cantidad": suma}))
                            await asyncio.sleep(0.5)

            elif tipo == "ficha_sacada":
                idx = data.get("indice")
                fichas_bot[idx] = {"posicion": data.get("posicion"), "activa": True}

            elif tipo == "ficha_movida":
                idx = data.get("indice")
                pos = data.get("nueva_posicion")
                fichas_bot[idx]["posicion"] = pos

            elif tipo == "ficha_llegada":
                idx = data.get("indice")
                fichas_bot[idx] = {"posicion": 100, "activa": False}

            elif tipo == "ficha_enviada_carcel":
                idx = data.get("indice")
                fichas_bot[idx] = {"posicion": -1, "activa": False}

if __name__ == "__main__":
    asyncio.run(jugar())
