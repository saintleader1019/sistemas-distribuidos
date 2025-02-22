import threading


class MyThread(threading.Thread):
    def __init__(self, primer_operador, segundo_operador, operacion):
        super(MyThread, self).__init__()
        self.primer_operador = primer_operador
        self.segundo_operador = segundo_operador
        self.suma_operadores = 0
        self.resta_operadores = 0
        self.multiplicacion_operadores = 0
        self.division_operadores = 0
        self.operacion = operacion
    
    def suma(self,primer_operador,segundo_operador):
        return primer_operador+segundo_operador
    
    def resta(self,primer_operador,segundo_operador):
        return primer_operador-segundo_operador
    
    def multiplicacion(self,primer_operador,segundo_operador):
        return primer_operador*segundo_operador
    
    def division(self,primer_operador,segundo_operador):
        return primer_operador/segundo_operador
    
    def run(self):
        if self.operacion== 0:
            self.suma_operadores=self.suma(self.primer_operador, self.segundo_operador)
        elif self.operacion== 1:
            self.resta_operadores=self.resta(self.primer_operador, self.segundo_operador)
        elif self.operacion== 2:
            self.multiplicacion_operadores=self.multiplicacion(self.primer_operador, self.segundo_operador)
        elif self.operacion== 3:
            self.division_operadores=self.division(self.primer_operador, self.segundo_operador)

if __name__ == "__main__":

    primer_operador = 10
    segundo_operador = 5
    threads = []

    for i in range(4):
        operacion = i
        t = MyThread(primer_operador, segundo_operador, operacion)
        t.start()
        threads.append(t)
		
    for t in threads:
        t.join() #termina ejecuion de hilos

    print ("la suma es: "+str(threads[0].suma_operadores))
    print ("la resta es: "+str(threads[1].resta_operadores))
    print ("la multiplicacion es: "+str(threads[2].multiplicacion_operadores))
    print ("la division es: "+str(threads[3].division_operadores))