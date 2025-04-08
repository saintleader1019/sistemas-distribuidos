import socket, json

Mi_socket = socket.socket()
Mi_socket.bind(("localhost", 8001))
Mi_socket.listen(1)
print("Soy el servidor, vamos a intercambiar mensajes!!!!!")

credenciales = ["santiago", 1234]

cli, addr = Mi_socket.accept()
request_json = cli.recv(1024).decode()

# Convertimos la cadena JSON a un diccionario
try:
    request = json.loads(request_json)
except json.JSONDecodeError:
    print("Error al recibir JSON del cliente.")
    cli.close()
    Mi_socket.close()
    exit()

# Verificamos las credenciales
if request["usuario"] == credenciales[0] and request["password"] == credenciales[1]:
    nombre = request["usuario"]

    info = {
        "nombre": nombre,
        "mensaje": f"Conectado con: {nombre}",
        "ip": addr[0],
        "puerto": addr[1],
        "saludo": f"Hola {nombre}, bienvenido al sistema."
    }

    json_data = json.dumps(info)
    cli.send(json_data.encode())
else:
    error = {"error": "Credenciales incorrectas. Acceso denegado."}
    cli.send(json.dumps(error).encode())

cli.close()
Mi_socket.close()