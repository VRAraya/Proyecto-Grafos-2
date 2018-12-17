#Estructura de dato: Nodo
#La clase Nodo contiene tres parametros: un str Nombre, un diccionario ordenado de transiciones y un booleano que indica si es un estado final

import collections  #Se importa la superclase Colecciones para utilizar los diccionarios ordenados
                    #Los diccionarios ordenados tienen la capacidad de recordar el orden en que se ingresan los objetos que contienen
class Nodo:

    def __init__(self, nombre, final): #El metodo constructor requiere un nombre y el booleano que indica si es un estado final
        self.nombre = nombre
        self.final = final
        self.transiciones = collections.OrderedDict()


    def AgregarTransicion(self, simbolo, destino):      #Metodo que agrega una transicion al nodo
        
        if not simbolo in self.transiciones:            #Si el simbolo no esta en el listado de transiciones lo creamos con una lista vacia
            self.transiciones[simbolo] = []
        
        if not destino in self.transiciones[simbolo]:   #Revisamos que no hayamos agregado la transicion antes y la agregamos
            self.transiciones[simbolo].append(destino)


    def ObtenerTransicion(self, simbolo):               #Metodo que obtiene la transicion para un simbolo en especifico
        
        if simbolo in self.transiciones:                #Si existen transiciones para el simbolo devolvemos el listado
            return self.transiciones[simbolo]
        
        else:                                           #En caso contrario devolvemos una lista vacia
            return []


    def RemueveTransicion(self, simbolo):               #Metodo que borra las transiciones para un simbolo en especifico
        
        del self.transiciones[simbolo]


    def ObtenerNombre(self):                            #Metodo que devuelve el nombre del nodo
        
        return self.nombre


    def ObtenerTransiciones(self):                      #Metodo que devuelve el listado completo de transiciones para el nodo
        
        return self.transiciones


    def EsFinal(self):                                  #Metodo que devuelve si el nodo es final
        
        return self.final


    def ModFinal(self, esfinal):                        #Metodo que modifica si el nodo es final
        
        self.final = esfinal


    def ModName(self, name):                            #Metodo que modifica el nombre del nodo
        
        self.name = name


    def ReemplazarTransicion(self, NodoValido, NodoDuplicado):          #Metodo que reemplaza un nodo por otro en las transiciones
        
        for simbolo, transicion in self.transiciones.items():              #Iteramos sobre las transiciones
            
            for index, nombreNodo in enumerate(transicion):
                
                if nombreNodo == NodoDuplicado:                         #Si el nodo es el duplicado lo reemplazamos por el valido
                    transicion[index] = NodoValido


    def __repr__(self):                                 #Metodo que muestra por consola el nodo con todos sus parametros
        
        return ("<Nodo id='%s', nombre='%s', esFinal='%s', transiciones='%s'>\n" % (hex(id(self)), self.nombre, self.final, self.transiciones))