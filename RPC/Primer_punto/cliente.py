import xmlrpc.client
import os

def seleccionar_nueva_opcion():
    input("\nPresione Enter para seleccionar otra opción...")
    limpiar_consola()  

def limpiar_consola():
    if os.name == 'nt': 
        os.system('cls')
        
def ingresar_datos_entrada():
    a =int(input('Ingrese el primer numero: '))
    b=int(input('Ingrese el segundo numero: '))
    return [a,b]
    



s = xmlrpc.client.ServerProxy('http://localhost:8001')

opcion = -1
while opcion != "g" :
    print("*************Menú Matemático******************************\n")
    print("a. Sumar")
    print("b. Restar")
    print("c. Multiplicar")
    print("d. Dividir")
    print("e. Potencia")
    print("f. Fibonacci")
    print("g. salir\n")

    opcion = str(input('Elija una opción: '))

    if opcion == "a":
        a,b = ingresar_datos_entrada()
        print("\nla suma es: " + str(s.suma(a,b)))
        seleccionar_nueva_opcion()

    elif opcion == "b":
       a,b = ingresar_datos_entrada()
       print("\nla resta es: " + str(s.resta(a,b)))
       seleccionar_nueva_opcion()

    elif opcion == "c":
       a,b = ingresar_datos_entrada()
       print("\nla multiplicacion es: " + str(s.multi(a,b)))
       seleccionar_nueva_opcion()

    elif opcion == "d":
       a,b = ingresar_datos_entrada()
       print("\nla division es: " + str(s.divi(a,b)))
       seleccionar_nueva_opcion()
       
    elif opcion == "e":
       a,b = ingresar_datos_entrada()
       print("\n el resultado de la potencia es: " + str(s.pot(a,b)))
       seleccionar_nueva_opcion()
       
    elif opcion == "f":
       a = int(input('Ingrese el numero de valores que desea  de la serie de Fibonacci:'))
       print("\n la serie de fibonacci solicitada es: " + str(s.fib(a,"0")))
       seleccionar_nueva_opcion()

    elif opcion == "g":
        break