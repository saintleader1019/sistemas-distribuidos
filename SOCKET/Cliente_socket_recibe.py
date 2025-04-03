import socket
import time 
s = socket.socket()   
s.connect(("localhost", 8001))
print("DATOS: ")
mensaje=input('ingresa tu nombre: ')
s.send(mensaje.encode())
mensaje_regreso=str(s.recv(1024))
print("Hola "+mensaje_regreso+" Bienvenido al sistema, como te sientes hoy?")
s.close()