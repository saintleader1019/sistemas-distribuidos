# -*- coding: utf-8 -*-
"""
clase sistemas distribuidos

@author: Usuario UTP
"""
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
from collections import Counter

class funciones_rpc:
    def comprobar_usuario(self, user, password):
        Datos_Usuario=["falcao","rayo2024"]
        if user == Datos_Usuario[0] and password == Datos_Usuario[1]:
            return 1
        else:
            return 0
    
    def invertir(self, p):
        return p[::-1]
    
    def repetido_lista(self, lista_numeros):
        contador = Counter(lista_numeros)
        return contador.most_common(1)[0][0]  # Retorna el número más repetido
    
    def enviar_archivo(self, lista_numeros):
        with open("procesado.txt", "w") as archivo:
            if isinstance(lista_numeros, list):  # Si es una lista
                for num in lista_numeros:
                    archivo.write(f"{num}\n")
            else:  # Si es un solo número
                archivo.write(f"{lista_numeros}\n")
                
        with open("procesado.txt", "rb") as archivo:
            respuesta_bin = xmlrpc.client.Binary(archivo.read())  # Convertir a binario para enviar
        return respuesta_bin

    
    def recibir_archivo(self, archivo_binario, nombre_archivo, choice):
        with open(nombre_archivo, "wb") as archivo:
            archivo.write(archivo_binario.data)  # Guardar los datos binarios en el archivo
        with open(nombre_archivo, "r") as archivo:
            lista_numeros = [int(linea.strip()) for linea in archivo.readlines()]
        # Aquí puedes realizar las operaciones que necesites, como invertir la lista o encontrar el repetido
        if choice == 1:
            lista_numeros = self.invertir(lista_numeros)
            return self.enviar_archivo(lista_numeros)
        elif choice == 2:
            lista_numeros = self.repetido_lista(lista_numeros)
            return self.enviar_archivo(lista_numeros)
        else:
            return "Opción no válida."

server = SimpleXMLRPCServer(("localhost", 8001))
server.register_instance(funciones_rpc())
print("soy un servidor implementado con clases")
server.serve_forever()