#Estructura de dato: Automata Finito (Puede ser Deterministico como No deterministico)
#La clase AF contiene tres parametros: un diccionario ordenado de nodos, una lista de simbolos y un nodo inicial

import collections      #Se importa la superclase Colecciones para utilizar los diccionarios ordenados
from Nodo import Nodo   #Se importa la clase Nodo desde el archivo Nodo.py

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
        for nombreNodo, nodo in self.nodos.items():                           #Iteramos sobre los nodos    
            for simbolo, transicion in nodo.ObtenerTransiciones().items():    #Iteramos sobre las transiciones del nodo para obtener los simbolos
                if (not simbolo in self.simbolos) and simbolo != "E":         #Si el simbolo aun no ha sido ingresado y no es "palabra vacia" lo agregamos a la lista
                    self.simbolos.append(simbolo)
                    self.simbolos.sort()                                      #Ordenamos la lista

    def esAFD(self):                                            #Metodo que revisa si el AF es AFD
        for nodoNombre, nodo in self.nodos.items():             #Iteramos sobre los nodos del AF
            transiciones = nodo.ObtenerTransiciones()           #Obtenemos las transiciones del nodo
            if len(transiciones) < len(self.simbolos):          #Si tiene transiciones para menos simbolos que los validos es un AFND
                return False
            for simbolo, destinos in transiciones.items():      #Revisamos cada transicion
                if len(str(simbolo)) > 1:                       #Si el simbolo tiene mas de un caracter es un AFND
                    return False
                if len(destinos) > 1:                           #Si para un simbolo tiene mas de una transicion es un AFND
                    return False
        return True                                             #Si ninguna de las condiciones anteriores fue verdadera, es un AFD

    def ConseguirClausura(self, nodos):                                     #Obtiene la clausura para un listado de nodos
        nuevosNodos = nodos[:]                                              #Creamos una copia de los nodos para verificar cambios al final
        for nodoNombre in nodos:                                            #Iteramos sobre los nodos
            nuevosNodos += self.nodos[nodoNombre].ObtenerTransiciones("E")  #Obtenemos todas las transiciones que se pueden hacer con la palabra vacia
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

        
    def aAFD(self):                                     #Metodo que transforma un AFND a un AFD
        if self.esAFD():                                #Si el AF ya es un AFD devolvemos la instancia
            return self
        tempNodoID = 1                                  #Iniciamos un contador para los nodos que usaremos para eliminar las secuencias con longitud mayor que 1
        for nodeName, node in self.nodes.iteritems():   #Iteramos sobre los nodos
            # Obtenemos las transiciones de cada nodo
            for symbol, transition in node.getTransitions().iteritems():
                # Revisamos si a secuencia tiene longitud mayor que 1
                if len(symbol) > 1:
                    # Invertimos la secuencia
                    reverseSymbol = symbol[::-1]

                    # Cada nodo que vayamos creando apuntara al ultimo creado
                    # en el primer caso es a la transicion completa del simbolo
                    lastNode = transition

                    # Seteamos una variable con el nombre del ultmo nodo temporal creado
                    # para usarlo en la transicion del nodo inicial
                    tempNodeName = None

                    # Leemos la secuencia invertida caracter a caracter, excepto por el ultimo
                    # (o sea, el primero de la secuencia) ya que ese lo usaremos en el nodo inicial
                    for i in range(0, (len(reverseSymbol) - 1)):
                        # Obtenemos el caracter de la secuencia
                        singleSymbol = reverseSymbol[i]

                        # Creamos un nodo temporal de nombre "tempID", donde ID lo obtenemos 
                        # de un contador incremental. El nodo no es final.
                        tempNodeName = "temp%s" % (tempNodoID)
                        tempNode = Node(tempNodeName, False)

                        # Si es la primera iteracion haremos la transicion desde el nodo
                        # a todos los que apuntaba la secuencia inicial, si es un una iteracion mayor
                        # apuntaremos el nodo al ultimo nodo temporal creado
                        for nextNode in lastNode:
                            tempNode.addTransition(singleSymbol, nextNode)

                        # Agregamos el nodo al AF
                        self.addNode(tempNode)

                        # Seteamos la variable lastNode con el nodo recien creado para la siguiente iteracion
                        lastNode = [tempNodeName]

                        #Aumentamos el contador del nodo intermedio
                        tempNodoID += 1

                    # Luego de desarmar la secuencia eliminamos la transicion del nodo original
                    # y creamos una transicion al ultimo nodo temporal creado
                    node.removeTransition(symbol)
                    node.addTransition(symbol[0], tempNodeName)

        # Actualizamos el listado de simbolos validos
        self.symbols = []
        self.updateSymbols()

        # Instanciamos un nuevo AF para el AFD
        newAF = AF()
        # Creamos un contados para los nombres de los nodos
        nodesCounter = 0
        # Creamos diccionarios para asociar grupos de nodos con su nombre y vice-versa
        nodeNameByTransitions = {}  # Get nodeName using the group of nodes
        transitionsByNodeName = {}  # Get group of Nodes using the nodeName
        # Creamos un directorio de nodos
        nodes = {}
        # Creamos una lista con los nuevos nodos que crearemos, como solo agregaremos
        # nodos no hay problemas en modificarlo mientras iteramos
        nodesToIterate = []

        # Asumimos que el primer nodo del AFD es el nodo inicial (Premisa)
        firstNode = self.nodes.itervalues().next()

        # Obtenemos la clausura del nodo inicial
        transitions = self._getClausura([firstNode.getName()])
        # Creamos un string con los nodos obtenidos en la clausura, porque las llaves de los
        # diccionarios no pueden ser mutables
        transitionString = '|'.join(str(v) for v in transitions)

        # Seteamos el nombre del nodo inicial
        nodeName = "Q" + str(nodesCounter)
        # Asociamos el nombre del nuevo nodo con los nodos primitivos que lo componen
        nodeNameByTransitions[transitionString] = nodeName
        transitionsByNodeName[nodeName] = transitions
        # Agregamos el nodo al listado de nodos por iterar
        nodesToIterate.append(nodeName)
        # Determinamos si el nuevo nodo sera final
        isFinal = self._newNodeIsFinal(transitions)

        # Creamos un nuevo nodo y lo agregamos al AFD
        node = Node(nodeName, isFinal)
        newAF.addNode(node)

        # Agregamos el nodo al listado de nodos usango el nombre como llave
        nodes[nodeName] = node

        # Aumentamos el contador de nodos
        nodesCounter += 1

        # Iteramos sobre los nodos que vamos creando
        for nodeToIterate in nodesToIterate:
            # Iteramos sobre los simbolos validos
            for symbol in self.symbols:
                # Obtenemos las transiciones de los nodos primitivos que componen el nuevo nodo
                # usando un simbolo especifico. Este metodo tambien devuelve la clausura.
                transitions = self._getTransitions(transitionsByNodeName[nodeToIterate], symbol)
                transitionString = '|'.join(str(v) for v in transitions)

                # Verificamos si tenemos un "nuevo nodo" compuesto por el listado
                # de "nodos primitivos" que obtuvimos
                if transitionString in nodeNameByTransitions:
                    # Si ya hemos creado el nuevo nodo solo agregamos la transicion
                    nodes[nodeToIterate].addTransition(symbol, nodeNameByTransitions[transitionString])
                else:
                    # Si no tenemos un "nodo nuevo" compuesto por el listado de nodos primitivos lo creamos
                    # Creamos el nombre del nodo usando el iterador
                    nodeName = "Q" + str(nodesCounter)
                    # Asociamos el nombre del nodo al listado de nodos primitivo y vice-versa
                    nodeNameByTransitions[transitionString] = nodeName
                    transitionsByNodeName[nodeName] = transitions
                    # Agregamos el nuevo nodo al listado de nodos por iterar
                    nodesToIterate.append(nodeName)
                    # Verificamos si el nuevo nodo va a ser final
                    isFinal = self._newNodeIsFinal(transitions)

                    # Creamos el nuevo nodo y lo agregamos al AFD
                    node = Node(nodeName, isFinal)
                    newAF.addNode(node)

                    # Agregamos el nuevo nodo al listado de nodos
                    nodes[nodeName] = node

                    # Aumentamos el contador de nuevos nodos
                    nodesCounter += 1

                    # Agregamos la transicion al nodo recien creado
                    nodes[nodeToIterate].addTransition(symbol, nodeName)

        # Actualizamos los simbolos validos en el AFD
        newAF.updateSymbols()

        # Devolvemos el AFD
        return newAF