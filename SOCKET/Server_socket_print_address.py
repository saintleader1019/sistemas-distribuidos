import socket, time, json

Mi_socket=socket.socket()
Mi_socket.bind(("localhost", 8001))
Mi_socket.listen(1)
print ("Soy el servido, vamos a intercambiar mensajes!!!!!")
cli, addr=Mi_socket.accept()
recibido = str(cli.recv(1024))
print("Conectado con: "+recibido)
print("te has conectado por la ip:"+str(addr[0]))
print("tu puerto es: "+str(addr[1]))
cli.send(recibido.encode())
cli.close()
Mi_socket.close()