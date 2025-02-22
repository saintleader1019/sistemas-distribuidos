import threading
import math

class MyThread(threading.Thread):
    def __init__(self, lista_a_operar):
        super(MyThread, self).__init__()
        self.lista_a_operar = lista_a_operar
        
        self.resultado_parcial = 0 # resultado parcial de la suma factorial
    
    def op_factorial(self,n):
        resultado = 1
        for i in range(1, n + 1):
            resultado *= i
        return resultado

    def suma_factorial(self,lista_a_operar):
        suma = 0
        factorial = 0
        tamano_lista = len(lista_a_operar)
        for i in range(tamano_lista):
            factorial = self.op_factorial(lista_a_operar[i])
            suma = suma + factorial
            
        return suma
            
            
    
    def run(self):
        
        self.resultado_parcial=self.suma_factorial(self.lista_a_operar)
        


if __name__ == "__main__":
    n =int(input('Ingrese el valor de n para suma de factoriales: '))
    hilos = int(input('ingrese la cantidad de hilos: '))
    relacion = math.floor(n/hilos)
    indicador = 1
    hilos_usados=1
    resultado = 0
    
    
        
    
    threads = [] #lista de hilos
    
    for i in range(hilos):
        lista_a_operar = []
        if hilos_usados < hilos:# condicional para agregar a la lista la cantidad de datos = relacion
            for i in range(relacion):
                lista_a_operar.append(indicador)
                indicador = indicador + 1
            hilos_usados = hilos_usados + 1
        elif hilos_usados == hilos:
            while indicador <= n :
                lista_a_operar.append(indicador)
                indicador = indicador + 1

            
        t = MyThread(lista_a_operar) #se crea hilo con atributos 
        t.start() #se inicia el hilo
        threads.append(t) #se guarda el hilo en la lista

    for t in threads:
        t.join() #termina ejecuion de hilos
    for h in range(hilos):
      #recoge tarea/trabajo(sumatoria) de los hilos en cada posion de la lista, atributo suma_parcial  
        resultado = resultado + threads[h].resultado_parcial

    print ("el resultado de la suma de factoriales es: " +str(resultado))

