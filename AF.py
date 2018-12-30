#Estructura de dato: Automata Finito (Puede ser Deterministico como No deterministico)
#La clase AF contiene tres parametros: un diccionario ordenado de nodos, una lista de simbolos y un nodo inicial

import collections      #Se importa la superclase Colecciones para utilizar los diccionarios ordenados
from Nodo import Nodo   #Se importa la clase Nodo desde el archivo Nodo.py
import copy             #Se importa copy

class AF:

    def __init__(self):             #El metodo constructor no requiere ningun argumento, e inicia los tres parametros vacios
        self.nodos = collections.OrderedDict()
        self.simbolos = []
        self.inicial = None


    def ObtenerNodos(self):         #Metodo que obtiene el diccionario de nodos que contiene el automata
        
        return self.nodos


    def ObtenerSimbolos(self):      #Metodo que obtiene el array de simbolos que acepta el automata
        
        return self.simbolos


    def ObtenerInicial(self):       #Metodo que obtiene el nodo inicial del automata
        
        return self.inicial
    

    def AgregarNodo(self, nodo):                    #Metodo que agrega un nodo al AF
        
        self.nodos[nodo.ObtenerNombre()] = nodo     #Agregamos el nodo al AF usando el nombre del nodo como llave
        
        if self.inicial is None:                    #Si es el primer nodo guardamos el nombre en self.inicial
            self.inicial = nodo.ObtenerNombre()     
        
        self.ActualizarSimbolos()                   #Actualizamos el listado de simbolos validos


    def ActualizarSimbolos(self):                                             #Metodo que actualiza el listado de simbolos validos
        
        for nombreNodo, nodo in iter(self.nodos.items()):                           #Iteramos sobre los nodos    
            
            for simbolo, transicion in iter(nodo.ObtenerTransiciones().items()):    #Iteramos sobre las transiciones del nodo para obtener los simbolos
                
                if (not simbolo in self.simbolos) and simbolo != "E":         #Si el simbolo aun no ha sido ingresado y no es "palabra vacia" lo agregamos a la lista
                    self.simbolos.append(simbolo)
                    self.simbolos.sort()                                      #Ordenamos la lista


    def esAFD(self):                                            #Metodo que revisa si el AF es AFD
        
        for nodoNombre, nodo in iter(self.nodos.items()):             #Iteramos sobre los nodos del AF
            transiciones = nodo.ObtenerTransiciones()           #Obtenemos las transiciones del nodo
            
            if len(transiciones) < len(self.simbolos):          #Si tiene transiciones para menos simbolos que los validos es un AFND
                return False
            
            for simbolo, destinos in iter(transiciones.items()):      #Revisamos cada transicion
                
                if len(str(simbolo)) > 1:                       #Si el simbolo tiene mas de un caracter es un AFND
                    return False
                
                if len(destinos) > 1:                           #Si para un simbolo tiene mas de una transicion es un AFND
                    return False
        return True                                             #Si ninguna de las condiciones anteriores fue verdadera, es un AFD


    def ConseguirClausura(self, nodos):                                     #Obtiene la clausura para un listado de nodos
        
        nuevosNodos = nodos[:]                                              #Creamos una copia de los nodos para verificar cambios al final
        
        for nodoNombre in nodos:                                            #Iteramos sobre los nodos
            nuevosNodos += self.nodos[nodoNombre].ObtenerTransicion("E")  #Obtenemos todas las transiciones que se pueden hacer con la palabra vacia
        
        nuevosNodos = list(set(nuevosNodos))                                #Eliminamos los nodos repetidos
        
        if sorted(nodos) != sorted(nuevosNodos):                            #Verificamos si hemos agregado nodos al listado inicial
            return self.ConseguirClausura(sorted(nuevosNodos))              #Si la lista es distinta llamamos nuevamente a la funcion con los nuevos nodos
        
        else:                                           
            return sorted(nuevosNodos)                                      #Si la lista es igual ya tenemos todos los nodos necesarios


    def ConseguirTransiciones(self, nodos, simbolo):                            #Obtiene todas las transiciones para un grupo de nodos usando cierto simbolo
        
        transiciones = []
        
        for nodoNombre in nodos:                                                #Iteramos sobre el listado de nodos                                                         
            transiciones += self.nodos[nodoNombre].ObtenerTransicion(simbolo)   #Buscamos todas las transiciones para el nodo usando el simbolo dado y lo agregamos al listado de transiciones anteriores
        
        transiciones = list(set(transiciones))                                  #Eliminamos los nodos duplicados
        return self.ConseguirClausura(transiciones)                             #Devolvemos la clausura de los nodos encontrados


    def nuevoNodoEsFinal(self, nodos):              #Determinamos si un "nuevo nodo" es final
        
        for nodoNombre in nodos:                    #Iteramos sobre los nodos, revisando si alguno de estos es final
            if self.nodos[nodoNombre].EsFinal():    #Si alguno es final entonces el nuevo nodo tambien lo es
                return True
        
        return False                                #En caso contrario no es un nodo final


    def ConvertirEnAFD(self):                           #Metodo que transforma un AFND a un AFD
        
        if self.esAFD():                                #Si el AF ya es un AFD devolvemos la instancia
            return self
        
        tempNodoID = 1                                  #Iniciamos un contador para los nodos que usaremos para eliminar las secuencias con longitud mayor que 1
        
        for nodoNombre, nodo in iter(self.nodos.items()):                             #Iteramos sobre los nodos
            for simbolo, transicion in iter(nodo.ObtenerTransiciones().items()):        #Obtenemos las transiciones de cada nodo                                                                  
                if len(simbolo) > 1:                                            #Revisamos si la secuencia tiene longitud mayor que 1
                    rsimbolo = simbolo[::-1]            #Invertimos la secuencia
                    ultimoNodo = transicion             #Cada nodo que vayamos creando apuntara al ultimo creado, en el primer caso es a la transicion completa del simbolo
                    tempNodoNombre = None               #Asignamos una variable con el nombre del ultimo nodo temporal creado para usarlo en la transicion del nodo inicial
                    for i in range(0, (len(rsimbolo) - 1)):                 #Leemos la secuencia invertida caracter a caracter, excepto por el ultimo (o sea, el primero de la secuencia) ya que ese lo usaremos en el nodo inicial
                        sSimbolo = rsimbolo[i]                              #Obtenemos el caracter de la secuencia
                        tempNodoNombre = "temp%s" % (tempNodoID)            #Creamos un nodo temporal de nombre "tempID", donde ID lo obtenemos del contador incremental. El nodo no es final.
                        tempNodo = Nodo(tempNodoNombre, False)
                        for siguienteNodo in ultimoNodo:                    #Si es la primera iteracion haremos la transicion desde el nodo a todos los que apuntaba la secuencia inicial, si es un una iteracion mayor apuntaremos el nodo al ultimo nodo temporal creado
                            tempNodo.AgregarTransicion(sSimbolo, siguienteNodo)
                        self.AgregarNodo(tempNodo)                          #Agregamos el nodo al AF
                        ultimoNodo = [tempNodoNombre]                       #Asignamos la variable ultimoNodo con el nodo recien creado para la siguiente iteracion
                        tempNodoID += 1                                     #Aumentamos el contador del nodo intermedio
                    nodo.RemueveTransicion(simbolo)                         #Luego de desarmar la secuencia eliminamos la transicion del nodo original y creamos una transicion al ultimo nodo temporal creado
                    nodo.AgregarTransicion(simbolo[0], tempNodoNombre)

        self.simbolos = []                              #Actualizamos el listado de simbolos validos
        self.ActualizarSimbolos()

        nuevoAF = AF()                                  #Instanciamos un nuevo AF para el AFD
        contadorNodos = 0                               #Creamos un contador para los nombres de los nodos
                                                        #Creamos diccionarios para asociar grupos de nodos con su nombre y viceversa

        nombreNodosporTransiciones = {}                 #Get nodoNombre using the group of nodos
        transicionesporNombreNodo = {}                  #Get group of nodos using the nodoNombre
        
        nodos = {}                                      #Creamos un diccionario de nodos
        nodosaIterar = []                               #Creamos una lista con los nuevos nodos que crearemos, como solo agregaremos nodos no hay problemas en modificarlo mientras iteramos

        primerNodo = next(iter(self.nodos.values()))    #Asumimos que el primer nodo del AFD es el nodo inicial (Premisa)

        transiciones = self.ConseguirClausura([primerNodo.ObtenerNombre()])     #Obtenemos la clausura del nodo inicial
        transicionString = '|'.join(str(v) for v in transiciones)               #Creamos un string con los nodos obtenidos en la clausura, porque las llaves de los diccionarios no pueden ser mutables

        nodoNombre = "Q" + str(contadorNodos)                                   #Asignamos el nombre del nodo inicial
        
        nombreNodosporTransiciones[transicionString] = nodoNombre               #Asociamos el nombre del nuevo nodo con los nodos primitivos que lo componen
        transicionesporNombreNodo[nodoNombre] = transiciones
        
        nodosaIterar.append(nodoNombre)                                         #Agregamos el nodo al listado de nodos por iterar 
        
        esFinal = self.nuevoNodoEsFinal(transiciones)                           #Determinamos si el nuevo nodo sera final

        nodo = Nodo(nodoNombre, esFinal)                                        #Creamos un nuevo nodo y lo agregamos al AFD    
        nuevoAF.AgregarNodo(nodo)

        nodos[nodoNombre] = nodo                                                #Agregamos el nodo al listado de nodos usando el nombre como llave

        contadorNodos += 1                                                      #Aumentamos el contador de nodos

        for nodoaIterar in nodosaIterar:                                        #Iteramos sobre los nodos que vamos creando
            for simbolo in self.simbolos:                                       #Iteramos sobre los simbolos validos
                
                transiciones = self.ConseguirTransiciones(transicionesporNombreNodo[nodoaIterar], simbolo)  #Obtenemos las transiciones de los nodos primitivos que componen el nuevo nodo usando un simbolo especifico. Este metodo tambien devuelve la clausura.
                transicionString = '|'.join(str(v) for v in transiciones)

                if transicionString in nombreNodosporTransiciones:                                              #Verificamos si tenemos un "nuevo nodo" compuesto por el listado de "nodos primitivos" que obtuvimos
                    nodos[nodoaIterar].AgregarTransicion(simbolo, nombreNodosporTransiciones[transicionString]) #Si ya hemos creado el nuevo nodo solo agregamos la transicion
                else:
                    nodoNombre = "Q" + str(contadorNodos)   #Si no tenemos un "nodo nuevo" compuesto por el listado de nodos primitivos, lo creamos, y creamos el nombre del nodo usando el iterador
                    
                    nombreNodosporTransiciones[transicionString] = nodoNombre   #Asociamos el nombre del nodo al listado de nodos primitivo y viceversa
                    transicionesporNombreNodo[nodoNombre] = transiciones
                    
                    nodosaIterar.append(nodoNombre)         #Agregamos el nuevo nodo al listado de nodos por iterar
                    
                    esFinal = self.nuevoNodoEsFinal(transiciones)               #Verificamos si el nuevo nodo va a ser final

                    nodo = Nodo(nodoNombre, esFinal)                            #Creamos el nuevo nodo y lo agregamos al AFD
                    nuevoAF.AgregarNodo(nodo)

                    nodos[nodoNombre] = nodo                                    #Agregamos el nuevo nodo al listado de nodos

                    contadorNodos += 1                                          #Aumentamos el contador de nodos

                    nodos[nodoaIterar].AgregarTransicion(simbolo,nodoNombre)   #Agregamos la transicion al nodo recien creado

        nuevoAF.ActualizarSimbolos()        #Actualizamos los simbolos validos en el AFD
        return nuevoAF  #Devolvemos el AFD


    def Minimizar(self):                #Metodo que minimiza un AFD
                        
        if self.esAFD():                #Verificamos que estamos minimizando un AFD
            
            grupos = {}                 #Creamos los grupos iniciales donde separaremos los nodos por finales y no finales
            gruposporNombre = {}

            for nombreNodo, nodo in iter(self.nodos.items()):   #Iteramos sobre los nodos

                grupoID = 1                                     #Si el nodo es no-final estara en el primer grupo
                if nodo.EsFinal():                              #Si es final estara en el segundo
                    grupoID = 2

                if not grupoID in grupos:                       #Si aun no creamos el grupo lo creamos con lista vacia
                    grupos[grupoID] = []

                grupos[grupoID].append(nodo)                    #Asociamos el nodo a un grupo en especifico y viceversa
                gruposporNombre[nodo.ObtenerNombre()] = grupoID

            self.MinimizarR(grupos, gruposporNombre)             #Ejecutamos el metodo recursivo que minimiza el AFD
        else:
            print ("No se puede minimizar un AFND")


    def MinimizarR(self, grupos, grupoporNombre):       #Metodo que minimiza recursivamente un AFD
        
        siguienteGrupoID = 1
        
        nuevosGrupos = {}                               #Creamos 2 diccionarios para los nuevos grupos de esta iteracion
        nuevoGrupoporNombre = {}

        for gID, grupo in iter(grupos.items()):         #Iteramos sobre los grupos recibidos como parametros
            
            grupoporTransiciones = {}                   #Creamos un diccionario para asociar un listado de transiciones a un grupo
                                                        #Lo reseteamos cada vez que iteramos sobre un nuevo grupo
            for nodo in grupo:                          #Iteramos sobre los nodos en un grupo
                
                transiciones = nodo.ObtenerTransiciones()   #Obtenemos las transiciones de un grupo

                transicionesOrdenadas = []                  #Creamos 2 listas para asociar las transiciones a los grupos recibidos como parametro
                Gruposdetransicion = []

                for simbolo in self.simbolos:                                   #Iteramos sobre los simbolos validos
                    transicionesOrdenadas.append(transiciones[simbolo][0])      #Obtenemos la transicion asociada al simbolo

                for transicion in transicionesOrdenadas:                        #Por cada transicion obtenida identificamos a que grupo pertenece
                    Gruposdetransicion.append(grupoporNombre[transicion])

                transicionString = '|'.join(str(v) for v in Gruposdetransicion) #Creamos un string con los grupos asociados a las transiciones

                if transicionString in grupoporTransiciones:                    #Si el string ya existe buscamos el id del nuevo grupo
                    grupoID = grupoporTransiciones[transicionString]
                else:
                    grupoID = siguienteGrupoID                                  #En caso contrario creamos un nuevo grupo
                    grupoporTransiciones[transicionString] = grupoID
                    nuevosGrupos[grupoID] = []

                    siguienteGrupoID += 1

                nuevosGrupos[grupoID].append(nodo)                              #Asociamos el nodo al nuevo grupo y viceversa
                nuevoGrupoporNombre[nodo.ObtenerNombre()] = grupoID

        if grupos == nuevosGrupos:                                              #Si el grupo recibido como parametro es igual al obtenido en la iteracion solo nos queda eliminar los duplicados
            self.EliminarDuplicados(nuevosGrupos)

        else:
            self.MinimizarR(nuevosGrupos, nuevoGrupoporNombre)                   #En caso contrario hacemos una nueva iteracion con los nuevos grupos


    def EliminarDuplicados(self, grupos):               #Metodo que elimina los nodos equivalentes despues de minimizar
        
        for grupoId, grupo in iter(grupos.items()):     #Iteramos sobre los grupos recibidos
            
            if len(grupo) > 1:                          #Si el grupo tiene mas de un nodo es un duplicado
                
                nodoValido = None
                
                for nodoDuplicado in grupo:
                    
                    if nodoValido is None:              #Si es el primer nodo del grupo diremos que es el valido
                        
                        nodoValido = nodoDuplicado
                    
                    else:
                                                       #En caso contrario lo eliminaremos del listado de nodos
                        del self.nodos[nodoDuplicado.ObtenerNombre()]
                        
                        for nombreNodo, nodo in iter(self.nodos.items()):   #Y reemplazamos la transicion en todos los nodos del AFD
                            nodo.ReemplazarTransicion(nodoValido.ObtenerNombre(), nodoDuplicado.ObtenerNombre())

    def validarCadena(self, cadena):                #Metodo que valida una cadena para el Automata Finito
        
        afd = self.ConvertirEnAFD()                 #Para evitar tener que recorrer un arbol con mas de una rama valida nos aseguramos que trabajaremos sobre un AFD
        inicio = afd.ObtenerInicial()               #Llamamos al metodo de analisis recursivo entregando el nombre del nodo inicial del AFD y la cadena

        return afd.validarCadenaR(cadena, inicio)

    
    def validarCadenaR(self, cadena, inicio):       #Metodo que analiza recursivamente si una cadena pertenece a un AFD partiendo desde un nodo dado
        
        if self.esAFD():                            #Verificamos que estamos trabajando sobre un AFD

            if len(cadena) == 0:                    #Si el largo es 0 significa que estamos en el fin de la recursion por lo que solo analizamos si el nodo "actual" es un estado final
                return self.nodos[inicio].EsFinal()

            siguienteSimbolo = cadena[0]            #Sacamos el valor del proximo simbolo a analizar
            
            transiciones = self.nodos[inicio].ObtenerTransicion(siguienteSimbolo)    #Buscamos la transicion del AFD para el siguiente simbolo

            if len(transiciones) > 0:               #Si tiene transicion obtenemos el nombre del siguiente nodo

                siguienteInicio = transiciones[0]

                return self.validarCadenaR(cadena[1:], siguienteInicio) #Llamamos al metodo de analisis recursivo con el resto de la palabra (sin el simbolo que acabamos de analizar) y el siguiente nodo
        
        return False

    def __repr__(self):             #Metodo que muestra por consola el AF con todos sus parametros
        print("<AF alfabeto: '%s', nodos: '\n%s'>" % (self.simbolos, self.nodos))
        return("<AF alfabeto: '%s', nodos: '\n%s'>" % (self.simbolos, self.nodos))

    def quintupla(self):        #Metodo que muestra por consola la quintupla del AF
        estados=[]
        estadosf=[]
        transicionesS=""
        for nombreNodo, nodo in iter(self.nodos.items()):
            estados.append(nombreNodo)
            if nodo.EsFinal():
                estadosf.append(nombreNodo)
            transiciones = nodo.ObtenerTransiciones()
            for simbolo, destinos in iter(transiciones.items()):
                for destino in destinos:
                    transicionesS+="("+nombreNodo+", "+simbolo+", "+destino+")"

        
        print("Estados: %s" %(estados))
        print("Alfabeto: %s" %(self.simbolos))
        print("Estado inicial: %s" %(self.inicial))
        print("Estados finales: %s" %(estadosf))
        print("Transiciones: "+ transicionesS)