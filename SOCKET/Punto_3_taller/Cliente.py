import socket
import threading

def recibir_mensajes(sock):
    while True:
        try:
            mensaje = sock.recv(1024).decode()
            if mensaje:
                print("\n" + mensaje)
            else:
                break
        except:
            print("❌ Error al recibir mensaje.")
            break

def cliente_chat():
    host = "localhost"
    puerto = 8001

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, puerto))

    nombre = input("🔑 Ingresa tu nombre: ")

    # Iniciar hilo para recibir mensajes
    hilo_recepcion = threading.Thread(target=recibir_mensajes, args=(sock,))
    hilo_recepcion.daemon = True
    hilo_recepcion.start()

    while True:
        mensaje = input()
        if mensaje.lower() == "salir":
            break
        sock.send(f"{nombre}: {mensaje}".encode())

    sock.close()

cliente_chat()
