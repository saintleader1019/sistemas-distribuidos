from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List, Dict
import random

app = FastAPI()

class ConexionJugador:
    def __init__(self, websocket: WebSocket, nombre: str, color: str):
        self.websocket = websocket
        self.nombre = nombre
        self.color = color
        self.fichas = [{"posicion": -1, "activa": False} for _ in range(4)]
        self.pares_consecutivos = 0

jugadores: List[ConexionJugador] = []
colores_disponibles = ["rojo", "azul", "verde", "amarillo"]
turno_actual = 0
partida_en_curso = False
casillas_seguras = [8, 13, 21, 26, 34, 39, 47, 52, 60, 65, 73, 78]

def casilla_salida(color: str):
    return {"rojo": 0, "verde": 19, "amarillo": 38, "azul": 57}.get(color, 0)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({"tipo": "solicitar_nombre"})
    try:
        datos = await websocket.receive_json()
        nombre = datos.get("nombre")

        if not nombre or len(jugadores) >= 4:
            await websocket.send_json({"tipo": "rechazo", "motivo": "Nombre inválido o máximo de jugadores alcanzado"})
            await websocket.close()
            return

        color = colores_disponibles.pop(0)
        jugador = ConexionJugador(websocket, nombre, color)
        jugadores.append(jugador)
        await websocket.send_json({"tipo": "confirmacion", "color": color})

        if len(jugadores) == 4:
            await iniciar_partida()

        while True:
            datos = await websocket.receive_json()
            await manejar_mensaje(jugador, datos)

    except WebSocketDisconnect:
        jugadores.remove(jugador)
        colores_disponibles.append(jugador.color)
        print(f"{jugador.nombre} desconectado")

def obtener_jugador_por_ws(ws: WebSocket):
    return next((j for j in jugadores if j.websocket == ws), None)

def siguiente_turno():
    global turno_actual
    turno_actual = (turno_actual + 1) % len(jugadores)
    return jugadores[turno_actual]

async def iniciar_partida():
    global partida_en_curso, turno_actual
    partida_en_curso = True
    random.shuffle(jugadores)
    turno_actual = 0
    for j in jugadores:
        await j.websocket.send_json({
            "tipo": "iniciar_partida",
            "jugadores": [p.nombre for p in jugadores],
            "turno_inicial": jugadores[turno_actual].nombre
        })
    await jugadores[turno_actual].websocket.send_json({"tipo": "tu_turno"})

async def manejar_mensaje(jugador: ConexionJugador, datos: Dict):
    global turno_actual

    if datos["tipo"] == "lanzar_dados":
        if jugadores[turno_actual] != jugador:
            await jugador.websocket.send_json({"tipo": "error", "mensaje": "No es tu turno"})
            return

        d1, d2 = random.randint(1,6), random.randint(1,6)
        par = d1 == d2

        await jugador.websocket.send_json({"tipo": "resultado_dados", "dado1": d1, "dado2": d2, "par": par})

        if par:
            jugador.pares_consecutivos += 1
            if jugador.pares_consecutivos == 3:
                await jugador.websocket.send_json({"tipo": "bonus_sacar_ficha", "mensaje": "Tres pares consecutivos"})
                jugador.pares_consecutivos = 0
            await jugador.websocket.send_json({"tipo": "tu_turno"})
        else:
            jugador.pares_consecutivos = 0
            siguiente = siguiente_turno()
            await siguiente.websocket.send_json({"tipo": "tu_turno"})

    elif datos["tipo"] == "sacar_ficha":
        idx = datos.get("indice_ficha")
        if idx is not None and 0 <= idx < 4:
            ficha = jugador.fichas[idx]
            if ficha["posicion"] == -1:
                ficha["posicion"] = casilla_salida(jugador.color)
                ficha["activa"] = True
                await jugador.websocket.send_json({"tipo": "ficha_sacada", "indice": idx, "posicion": ficha["posicion"]})

    elif datos["tipo"] == "mover_ficha":
        idx = datos.get("indice_ficha")
        cantidad = datos.get("cantidad")
        if idx is not None and cantidad is not None:
            ficha = jugador.fichas[idx]
            if ficha["posicion"] != -1:
                nueva = ficha["posicion"] + cantidad
                if nueva >= 76:
                    ficha["posicion"] = 100
                    ficha["activa"] = False
                    await jugador.websocket.send_json({"tipo": "ficha_llegada", "indice": idx})
                else:
                    ficha["posicion"] = nueva
                    await jugador.websocket.send_json({"tipo": "ficha_movida", "indice": idx, "nueva_posicion": nueva})

                    if nueva not in casillas_seguras:
                        for enemigo in jugadores:
                            if enemigo != jugador:
                                for i, ficha_enemiga in enumerate(enemigo.fichas):
                                    if ficha_enemiga["posicion"] == nueva:
                                        ficha_enemiga["posicion"] = -1
                                        ficha_enemiga["activa"] = False
                                        await enemigo.websocket.send_json({"tipo": "ficha_enviada_carcel", "indice": i, "por": jugador.nombre})
                                        await jugador.websocket.send_json({"tipo": "captura_realizada", "indice": idx, "enemigo": enemigo.nombre})

                # Verificar victoria
                if all(f["posicion"] == 100 for f in jugador.fichas):
                    for j in jugadores:
                        await j.websocket.send_json({"tipo": "juego_terminado", "ganador": jugador.nombre})
                    return

                siguiente = siguiente_turno()
                await siguiente.websocket.send_json({"tipo": "tu_turno"})
