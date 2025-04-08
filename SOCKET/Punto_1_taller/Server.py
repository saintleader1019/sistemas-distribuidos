import socket, json

Mi_socket = socket.socket()
Mi_socket.bind(("localhost", 8001))
Mi_socket.listen(1)
print("Soy el servidor, vamos a intercambiar mensajes!!!!!")

cli, addr = Mi_socket.accept()

nombre = cli.recv(1024).decode()

info = {
    "nombre": nombre,
    "mensaje": f"Conectado con: {nombre}",
    "ip": addr[0],
    "puerto": addr[1],
    "saludo": f"Hola {nombre}, bienvenido al sistema."
}

json_data = json.dumps(info)
cli.send(json_data.encode())

cli.close()
Mi_socket.close()