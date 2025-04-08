import socket
import threading

clientes = []

def manejar_cliente(cliente, direccion):
    print(f"🟢 Nueva conexión desde {direccion}")
    while True:
        try:
            mensaje = cliente.recv(1024).decode()
            if not mensaje:
                break
            print(f"📨 Mensaje de {direccion}: {mensaje}")
            # Enviar el mensaje a todos los demás clientes
            broadcast(f"{direccion[0]}:{direccion[1]} dice: {mensaje}", cliente)
        except:
            break

    print(f"🔴 Cliente desconectado: {direccion}")
    clientes.remove(cliente)
    cliente.close()

def broadcast(mensaje, origen):
    for c in clientes:
        if c != origen:
            try:
                c.send(mensaje.encode())
            except:
                pass  # Por si falla un envío

def iniciar_servidor():
    host = "localhost"
    puerto = 8001
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host, puerto))
    servidor.listen()

    print(f"🚀 Servidor escuchando en {host}:{puerto}...")

    while True:
        cliente, direccion = servidor.accept()
        clientes.append(cliente)
        hilo = threading.Thread(target=manejar_cliente, args=(cliente, direccion))
        hilo.start()

iniciar_servidor()
