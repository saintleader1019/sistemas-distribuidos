import socket
import json

s = socket.socket()
s.connect(("localhost", 8001))

usuario = str(input("Ingresa tu nombre: "))
password = int(input("Ingresa tu contraseña: "))

mensaje = json.dumps({"usuario": usuario, "password": password})

s.send(mensaje.encode())

# Recibimos y decodificamos el JSON
respuesta = s.recv(1024).decode()

# Verificamos si la respuesta está vacía
if not respuesta:
    print("Error: No se recibió respuesta del servidor.")
else:
    try:
        datos = json.loads(respuesta)
        
        # Verificamos si hay un error en la respuesta
        if "error" in datos:
            print("\n❌ Error del servidor:", datos["error"])
        else:
            # Imprimimos los datos de forma organizada
            print("\n--- Información recibida del servidor ---")
            print("Nombre:", datos["nombre"])
            print("IP:", datos["ip"])
            print("Puerto:", datos["puerto"])
            print("Mensaje:", datos["mensaje"])
            print("Saludo:", datos["saludo"])
    except json.JSONDecodeError:
        print("Error al decodificar la respuesta del servidor.")

s.close()
