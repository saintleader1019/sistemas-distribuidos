import threading


class MyThread(threading.Thread):
    def __init__(self, secuencia, limite, indices):
        super(MyThread, self).__init__()
        self.secuencia = secuencia #array con la cantidad de numeros a sumar de la secuencia. (10 en este caso)
        self.limite = limite
        self.indices = indices
        self.suma_parcial=0 # atributo para asignar la suma desde origen a destino
    
    def suma_rango(self,secuencia,limite, indices):
        #funcion que retorna la sumatoria desde el rango origen a destino
        suma=0
        for dato in range(limite):
            suma += secuencia**(indices[0])
            self.indices.pop(0)
        return suma
    
    def run(self):
        #se asigna al atributo suma_parcial del rango origen a destino en el hilo
        self.suma_parcial=self.suma_rango(self.secuencia, self.limite, self.indices)

if __name__ == "__main__":

    secuencia = 2 #lista de secuencia
    indices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] #lista de indices
    limite = int((len(indices)/5)) #limite de la secuencia
    suma=0 #variable para sumatoria total
    threads = [] #lista de hilos
    for i in range(5):
        
        t = MyThread(secuencia, limite, indices) #se crea hilo con atributos origen y destino
        t.start() #se inicia el hilo
        threads.append(t) #se guarda el hilo en la lista
		
    for t in threads:
        t.join() #termina ejecuion de hilos
    for h in range(5):
      #recoge tarea/trabajo(sumatoria) de los hilos en cada posion de la lista, atributo suma_parcial  
        suma=suma+threads[h].suma_parcial 
    print ("la suma es: "+str(suma))