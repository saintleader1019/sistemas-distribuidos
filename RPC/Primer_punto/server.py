# -*- coding: utf-8 -*-
"""
clase sistemas distribuidos

@author: Usuario UTP
"""
from xmlrpc.server import SimpleXMLRPCServer
class funciones_rpc:
    def suma(self, p, q):
        return p+q
    def resta(self, p, q):
        return p-q

    def multi(self, p, q):
        return p*q
    
    def divi(self, p, q):
        return p/q
    
    def pot(self, p, q):
        return p ** q
    
    def fib(self, p, q):
        lista_fib =[]
        n1=1
        n2=1
        aux = 0
        cont=0
        lista_fib.append(n1)
        lista_fib.append(n2)
        while cont <= p-3 :
            aux = n2
            n2 = n1 + n2
            lista_fib.append(n2)
            n1 = aux
            cont = cont + 1
        
        return lista_fib
    
server = SimpleXMLRPCServer(("localhost", 8001))
server.register_instance(funciones_rpc())
print("soy un servidor implementado con clases")
server.serve_forever()
