#Programa Principal: Menu por Consola

import os               #Se importa la libreria os
import sys
import collections      #Se importa la superclase Colecciones para utilizar los diccionarios ordenados
from Nodo import Nodo   #Se importa la clase Nodo desde el archivo Nodo.py
import copy             #Se importa copy
from AF import AF

def lee_entero():       #Pide un valor entero y lo devuelve, mientras no sea un valor valido, lo vuelve a pedir.
    while True:
        valor = input("")
        try:
            valor = int(valor)
            return valor
        except ValueError:
            print("ATENCION: Debe ingresar un numero entero.")

def lee_SN():       #Pide un S o N según corresponda, lo devuelve, mientras no sea S o N, lo vuelve a pedir.
    while True:
        opcion = input("(S/N): ").upper()
        if opcion in ["S", "N"]:
            return opcion

def limpiarPantalla():      #Limpia la pantalla dependiendo del sistema operativo
    import os
    if os.name == "nt":
        os.system("cls")
    elif os.name == "posix":
        os.system("clear")
    else:
        raise("No se puede limpiar la pantalla")
        print("<-No se pudo borrar la pantalla->")

def ingresar_nombre():
    nombre = input("Ingrese un nombre para el nuevo automata: ")
    try:
        nombre = str(nombre)
        return nombre
    except ValueError:
        print("ATENCION: Ingrese un nombre valido.")

def ingresar_alfabeto():
    print("\nIngrese cantidad de caracteres del alfabeto: ")
    caract=lee_entero()
    c=1
    global E
    E=[]
    while c<=caract:
        carac=input("* Ingrese caracter " + '%s: '%c)        
        if(carac in E):
            print("Ese caracter ya existe en el alfabeto del automata")
        else:
            c+=1
            E.append(carac)       
    print(E)

def ingresar_alfabetoAFND():
    print("\nIngrese cantidad de caracteres del alfabeto: ")
    caract=lee_entero()
    c=1
    global E
    E=[]
    E.append("E")
    while c<=caract:
        carac=input("* Ingrese caracter " + '%s: '%c)        
        if(carac in E):
            print("Ese caracter ya existe en el alfabeto del automata")
        else:
            c+=1
            E.append(carac)       
    print(E)

def ingresar_estados():
    print("\nIngrese cantidad de estados: ")
    estados=lee_entero()
    c1=1
    e=1
    x=1
    y=1
    global K
    global S
    global F
    K=[] 
    S=[]
    F=[]
    while c1<=estados:
        e=input("* Ingrese nombre al estado " + '%s: '%c1)
        if(e in K):
            print(" - Ingrese otro nombre de estado diferente - ")
        else:
            K.append(e)
            c1+=1
    print(K)
    print("\n")

##  ACA SE INGRESA LOS ESTADOS INICIALES
 
    while (x<=1):
        estadoI=input("* Ingrese estado inicial: ")
        if (estadoI in K):
            p = S.append(estadoI)
            if((p in K)!=estadoI):
                x+=1
                print("Estado inicial agregado.")
        else:
            print ("Ingrese Estado Inicial Valido")
                                                       
    print(S)
    print("\n")
   
    
##  ACA SE INGRESA LOS ESTADOS FINALES
    Festado=int(input("Ingrese cantidad de estados Finales: "))
    es=len(K) #LARGO DE LA CADENA DE ESTADOS
    if(Festado>es):
        while (Festado>es):
            print("Ingrese un numero menor o igual a: " + '%s'%estados)
            Festado=int(input("Ingrese cantidad de estados Finales: "))
        if(Festado <=es):
            while (y<=Festado):
                estadoF=input("* Ingrese estado Final: ")
                if (estadoF in K):
                    if(estadoF in F):
                        print(" - Ingrese otro Estado Final -")
                    else:
                        F.append(estadoF)                                           
                        y+=1
                        print("Estado Final agregado.")
                        
                else:
                    print(" - Ingrese otro Estado Final -")
                    
            print(F)
            print("\n")
    else:
        while (y<=Festado):
            estadoF=input("* Ingrese estado Final: ")
            if (estadoF in K):
                if(estadoF in F):
                    print(" - Ingrese otro Estado Final -")
                else:
                    F.append(estadoF)                                           
                    y+=1
                    print("Estado Final agregado.")                        
            else:
                print(" - Ingrese otro Estado Final -")
                    
    print(F)
    print("\n")

def escribirAF():                                ##LLENAMOS FICHERO
    
    nombre = ingresar_nombre()
    manejador=open(nombre,"w")

    estados = K
    estadoinicial = S
    estadosfinales = F
    simbolos = E

    if estadoinicial[0]!=estados[0]:          #Si el estado inicial no es el primero en la lista de estados, se coloca al inicio de la lista
        i=estados.index(estadoinicial[0])
        estados.insert(0, estadoinicial[0])
        estados.pop(i+1)
    
    for estado in estados:                      #Iteramos sobre los estados
        linea = "%s %s" % (estado, "S" if estado in estadosfinales else "N")    # Creamos un string con los 2 primeros parametros del estado, el nombre y si es final o no
        #ASIGNAMOS POR TECLADO LAS TRANSICIONES
        c=True
        
        while(c):
            transiciones = input("Ingrese todas las transiciones del estado %s, separadas con una coma (caracter del alfabeto:estado destino): " %(estado))
            transiciones = transiciones.split(",")

            for transicion in transiciones:
                transicion = transicion.split(":")
                if not transicion[0] in simbolos or not transicion[1] in estados:
                    print("Transicion para %s no valida, ingrese nuevamente." %(transicion[0]))
                    c=True
                else:
                    print("Transicion para %s valida." %(transicion[0]))
                    c=False

        for transicion in transiciones:
            linea += " %s" % (transicion)

        linea += "\n"           # Se agrega un salto de linea y se escribe en el archivo
        manejador.write(linea)

    # Metodo que carga un AF desde un archivo
def cargardesdeArchivo(af, nombreArchivo):
    
    if not os.path.isfile(nombreArchivo):
        print ("El archivo indicado no existe.")
        sys.exit()
        
    f = open(nombreArchivo)
    
    for linea in f:  # Leemos el archivo linea a linea
        linea = linea.rstrip()    # Removemos el salto de linea final
        
        data = linea.split()     # Dividimos la linea usando un espacio como separacion
        
        if len(data) > 1:          #Verificamos que tenga mas de 1 parametro (Se requiere por lo menos el nombre y si es final o no)
            nombreNodo = data[0]   #Usamos la primera palabra como nombre del nodo
            
            final = True if data[1] == "S" else False   #Usamos la segunda palabra para verificar si es un nodo final o no: Si es "S", es final, en otro caso no lo es
            
            nodo = Nodo(nombreNodo, final)  #Creamos el nodo con esos 2 parametros y los borramos de la lista, para luego iterar sobre las transiciones
            
            del data[:1]
            
            # Analizamos transicion a transicion
            
            for transicion in data: # Separamos la palabra usando ":", si la lista resultante tiene 2 entradas (Simbolo y estado al que avanza)
                transicion = transicion.split(":")
                if len(transicion) == 2:    # Si es valido se agrega la transicion al nodo
                    nodo.AgregarTransicion(transicion[0], transicion[1])
                    
            af.AgregarNodo(nodo)        # Se agrega el nodo al AF

        
def escribirEnArchivo(af, nombreArchivo):   # Metodo que escribe un AF en un archivo
    f = open(nombreArchivo, "w")
    
    for nombreNodo, node in iter(af.ObtenerNodos().items()):                # Iteramos sobre los nodos del AF
        linea = "%s %s" % (node.ObtenerNombre(), "S" if node.EsFinal() else "N")   # Creamos un string con los 2 primeros parametros del nodo, el nombre y si es final o no
        
        
        for simbolo, transicion in iter(node.ObtenerTransiciones().items()):      # Recorremos todas las transiciones del nodo
            for nodoDestino in transicion:
                linea += " %s:%s" % (simbolo, nodoDestino)    # Agregamos cada transicion al string que se imprimira
            
        linea += "\n"        #Se agrega un salto de linea y se escribe en el archivo
        f.write(linea)
        
    f.close()       # Se cierra el archivo


##   ::::::::::::::::::::: DEBAJO DE ESTO SE INVOCAN SOLO LAS FUNCIONES, ARRIBA SE COLOCAN LAS FUNCIONES ::::::::::::::::::::::::::::::

limpiarPantalla()

print("--PROGRAMA AUTOMATAS AFD - AFN--")
print(" ")
print(" ")

opcion=10

while opcion !=0:

    if opcion != 10:
        limpiarPantalla()

    print("1. Ingresar y guardar un automata nuevo")
    print("2. Cargar automata")
    print("0. Salir")

    print("Seleccione una opcion: ")
    opcion = lee_entero()

    while (opcion > 2) or (opcion < 0) :
        print("Ingrese una opcion valida.")
        print("Seleccione una opcion: ")
        opcion = lee_entero()
    
    if(opcion == 1):
        opcion11 = 10

        while opcion11 != 0:
            
            limpiarPantalla()

            print("1. Ingresar AFD")
            print("2. Ingresar AFND")
            print("0. Salir")

            print("Seleccione una opcion: ")
            opcion11 = lee_entero()

            while (opcion > 2) or (opcion < 0):
                print("Ingrese una opcion valida.")
                print("Seleccione una opcion: ")
                opcion11 = lee_entero()

            if(opcion11 == 1):
                ingresar_alfabeto()
                ingresar_estados()
                escribirAF()
                input("Pulsa una tecla para continuar")

            elif(opcion11 == 2):
                ingresar_alfabetoAFND()
                ingresar_estados()
                escribirAF()
                input("Pulsa una tecla para continuar")

    elif(opcion == 2):
        af = AF()
        nombreArchivoAF = input("Ingrese el nombre del AF guardado: ")
        cargardesdeArchivo(af, nombreArchivoAF)
        print("Automata Cargado")
        input("Pulsa una tecla para continuar")
        
        opcion2 = 10

        while opcion2 !=0:

            limpiarPantalla()
            print("Automata: %s" %(nombreArchivoAF))
            print("1. Visualizar la quintupla del AFD")
            print("2. Validar cadena con el AFD")
            print("3. Obtener el AFD equivalente, si es AFND")
            print("4. Obtener el AFD minimo")
            print("0. Salir")

            print("Seleccione una opcion: ")
            opcion2 = lee_entero()

            while (opcion2 > 4) or (opcion2 < 0):
                print("Ingrese una opcion valida.")
                print("Seleccione una opcion: ")
                opcion2 = lee_entero()

            if(opcion2 == 1):
                af.quintupla()
                input("Pulsa una tecla para continuar")

            elif(opcion2 == 2):
                cadena = input("Ingrese cadena a validar: ")
                esValida = af.validarCadena(cadena)
                
                if(esValida):
                    print("La secuencia %s es valida para el automata %s." %(cadena, nombreArchivoAF))
                else:
                    print("La secuencia %s no es valida para el automata %s." %(cadena, nombreArchivoAF))
                
                input("Pulsa una tecla para continuar")

            elif(opcion2 == 3):
                if(af.esAFD()):
                    print("%s es un automata finito deterministico, no requiere conversion." %(nombreArchivoAF))
                else:
                    nuevoAFD=AF()
                    nuevoAFD=af.ConvertirEnAFD()
                    escribirEnArchivo(nuevoAFD, nombreArchivoAF+"convertidoAFD")
                    print("Automata %s convertido a AFD" %(nombreArchivoAF))

                    print("¿Desea cargar el AFD resultante?: ")
                    opcion22 = lee_SN()

                    if (opcion22 == "S"):
                        af = nuevoAFD
                        nombreArchivoAF = nombreArchivoAF+"convertidoAFD"
                        print("Automata Cargado")
                    
                input("Pulsa una tecla para continuar")

            elif(opcion2 == 4):
                if(af.esAFD()):
                    nuevoAFDminimo=AF()
                    nuevoAFDminimo=af
                    nuevoAFDminimo.Minimizar()
                    escribirEnArchivo(nuevoAFDminimo, nombreArchivoAF+"minimizado")
                    print("Automata %s minimizado" %(nombreArchivoAF))

                    print("¿Desea cargar el AFD minimizado?: ")
                    opcion23 = lee_SN()

                    if (opcion23 == "S"):
                        af = nuevoAFD
                        nombreArchivoAF = nombreArchivoAF+"minimizado"
                        print("Automata Cargado")
                else:
                    print("No se puede minimizar un AFND, conviertelo en AFD primero")

                input("Pulsa una tecla para continuar")
