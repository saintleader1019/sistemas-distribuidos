import socket  
 
s = socket.socket()   
s.connect(("192.168.61.48", 8001))  
mensaje=str(input('ingrese el mensaje: '))
s.send(mensaje.encode()) 
s.close()