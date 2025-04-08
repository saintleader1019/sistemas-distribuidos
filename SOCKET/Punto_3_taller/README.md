## 🧬 3.1 Implementación de un servidor concurrente con hilos y sockets

Para permitir múltiples clientes conectados simultáneamente, se utiliza programación concurrente con **hilos (threads)** junto con **sockets**. Cada cliente es atendido en un hilo independiente, lo que permite que el servidor maneje múltiples conexiones activas al mismo tiempo sin bloquearse.

### 💠 ¿Cómo funciona?

- El **servidor** escucha conexiones entrantes.
- Por cada nueva conexión, se crea un **nuevo hilo** que se encarga de recibir y manejar los mensajes del cliente.
- Esto permite que varios clientes estén conectados y comunicándose **al mismo tiempo** de manera eficiente.

### 📦 Código del servidor concurrente

```python
import socket
import threading

# Lista para guardar todos los clientes conectados
clientes = []

# Función para manejar la comunicación con un cliente
def manejar_cliente(cliente, direccion):
    print(f"🟢 Conectado con {direccion}")
    while True:
        try:
            mensaje = cliente.recv(1024).decode()
            if not mensaje:
                break
            print(f"📨 Mensaje recibido de {direccion}: {mensaje}")
            # Reenviar el mensaje a todos los demás clientes
            broadcast(f"{direccion[0]}:{direccion[1]} dice: {mensaje}", cliente)
        except:
            break

    print(f"🔴 Cliente desconectado: {direccion}")
    clientes.remove(cliente)
    cliente.close()

# Función para enviar un mensaje a todos los clientes conectados excepto el emisor
def broadcast(mensaje, origen):
    for c in clientes:
        if c != origen:
            try:
                c.send(mensaje.encode())
            except:
                pass  # Ignorar si falla el envío

# Función principal del servidor
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

# Ejecutar el servidor
iniciar_servidor()
```

---

Con esta implementación, el servidor puede atender múltiples clientes de manera simultánea, siendo cada cliente manejado por un hilo distinto. Esto es esencial para construir sistemas de comunicación como chats, juegos multijugador o cualquier aplicación cliente-servidor con concurrencia.