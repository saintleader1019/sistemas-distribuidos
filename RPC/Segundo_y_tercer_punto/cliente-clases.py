import xmlrpc.client

# Función para que el usuario ingrese 10 números
def ingresar_numeros():
    numeros = []
    for i in range(10):
        num = int(input(f"Ingrese el número {i+1}: "))
        numeros.append(num)
    return numeros

# Función para guardar la lista en un archivo de texto
def guardar_en_txt(numeros, nombre_archivo):
    with open(nombre_archivo, "w") as archivo:
        for num in numeros:
            archivo.write(f"{num}\n")  # Guardamos cada número en una línea del archivo
    print(f"Archivo {nombre_archivo} guardado con éxito.")

# Conexión al servidor XML-RPC
s = xmlrpc.client.ServerProxy('http://localhost:8001')
def recibir_archivo(archivo_binario):
    with open("respuesta.txt", "wb") as archivo:
        archivo.write(archivo_binario.data)  # Guardar los datos binarios en el archivo
    with open("respuesta.txt", "r") as archivo:
        lista_numeros = [int(linea.strip()) for linea in archivo.readlines()]
    print(f"Lista procesada: {lista_numeros}")

# Función para enviar el archivo al servidor
def enviar_archivo(nombre_archivo, choice):
    with open(nombre_archivo, "rb") as archivo:
        archivo_binario = xmlrpc.client.Binary(archivo.read())  # Convertir a binario
    respuesta = s.recibir_archivo(archivo_binario, "lista.txt", choice)  # Enviar el archivo al servidor
    recibir_archivo(respuesta)

def acceso_cliente():
    numeros = ingresar_numeros()  # El cliente ingresa los 10 números
    guardar_en_txt(numeros, "data.txt")  # Guardamos la lista en un archivo de texto
    choice = int(input("Ingrese 1 para invertir la lista o 2 para encontrar el número repetido: "))
    enviar_archivo("data.txt", choice)  # Enviamos el archivo al servidor

# Ejecución del cliente
if __name__ == "__main__":
    user = str(input("Ingrese su nombre de usuario: "))
    password = str(input("Ingrese su contraseña: "))
    if s.comprobar_usuario(user, password) == 1:
        acceso_cliente()
    else:
        print("usuario o contraseña incorrecta, intente nuevamente")