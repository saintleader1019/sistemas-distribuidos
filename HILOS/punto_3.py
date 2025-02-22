import random
import threading

class MyThread(threading.Thread):
    def __init__(self, numero_1,numero_2):
        super(MyThread, self).__init__()
        self.numero_1 = numero_1 #atributo inicio del rango la suma se debe enviar en constructor
        self.numero_2 = numero_2 #atributo final del rango la suma se debe enviar en el constructor 
        self.suma_parcial=0 # atributo para asignar la suma desde origen a destino
    def suma_numeros_exp(self,numero_1,numero_2):
        suma_result = pow(numero_1,2)+ pow(numero_2,2)
        return suma_result   
    
    def run(self):
        #se asigna al atributo suma_parcial del rango origen a destino en el hilo
        self.suma_parcial=self.suma_numeros_exp(self.numero_1,self.numero_2)

if __name__ == "__main__":
    
    vector_aleatorio = []
    suma = 0
    norma_vector = 0
    Tamano_vector = 20
    
    # Llenar la lista con 20 posiciones
    for i in range(Tamano_vector):
        vector_aleatorio.append(random.randint(1, 100))  
        
    
    threads = [] #lista de hilos
    for i in range(10):
        
        t = MyThread(vector_aleatorio[i*2],vector_aleatorio[((i*2)+1)]) #se crea hilo con atributos 
        t.start() #se inicia el hilo
        threads.append(t) #se guarda el hilo en la lista
	
    for t in threads:
        t.join() #termina ejecuion de hilos
    for h in range(10):
      #recoge tarea/trabajo(sumatoria) de los hilos en cada posion de la lista, atributo suma_parcial  
        suma = suma + threads[h].suma_parcial 
    norma_vector = pow(suma,0.5)
    print ("la norma del vector : "+ str(vector_aleatorio) + " es: " +str(norma_vector))
  