import socket
import json

s = socket.socket()
s.connect(("localhost", 8001))

mensaje = input("Ingresa tu nombre: ")
s.send(mensaje.encode())

# Recibimos y decodificamos el JSON
datos = json.loads(s.recv(1024).decode())

# Imprimimos los datos de forma organizada
print("\n--- Información recibida del servidor ---")
print("Nombre:", datos["nombre"])
print("IP:", datos["ip"])
print("Puerto:", datos["puerto"])
print("Mensaje:", datos["mensaje"])
print("Saludo:", datos["saludo"])

s.close()
