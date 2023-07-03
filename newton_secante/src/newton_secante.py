import math as m
import matplotlib.pyplot as plt
import numpy as np
"""
El objetivo de este tp es aproximar raíces combinando el método Secante más el de Newton Raphson 
intercalando entre uno y otro, a mi equipo y a mi nos pareció más interesante comenzar con el método 
de Newton Raphson porque solo necesitamos pedirle al usuario un número inicial. 
El programa pide al usuario un número cercano a la raíz y la cantidad de decimales exactos que desa. 
Con estos datos el programa realiza la cantidad de iteraciones que necesite para conseguir un número(raíz) 
que tenga los decimales exactos indicados por el usuario. El lenguaje de programación seleccionado es 
python 3.10.6, las funciones a las que se desea someter el método tienen que ser asignadas en el código
fuente y verificar que cumplan con las condiciones que pide cada método si desea garantizar la convergencia.

por defecto tiene seteada la funcion función e^(-x)-sin(x) con su derivada -cos(x)-e^(-x)
"""

def f(x):
    return m.exp(-x)-m.sin(x)

def f1(x):
    return -m.cos(x)-m.exp(-x)

def decimal_truncate(numero, decimales):
    if (decimales < 0): raise Exception("el N° de decimales a truncar debe ser positivo")
    factor = 10.0 ** decimales
    return m.trunc(numero * factor) / factor

def grafico(numeroInicial,raizAproximada):
    DOMINIO = 4
    #genero datos para el dominio de x
    x_values = np.arange(numeroInicial-DOMINIO,numeroInicial+DOMINIO,step=0.3)
    #genero datos para el domino de y
    y_values = ([f(x) for x in x_values])
    #ploteo el grafico
    plt.plot(x_values,y_values)
    # Agregar el eje de abscisas
    plt.axhline(y=0, color='black', linestyle='--')
    # Agregar el eje de ordenadas
    plt.axvline(x=0, color='black', linestyle='--')
    #agrego puntos calulados 
    plt.scatter(raizAproximada,f(raizAproximada),c="red")
    #agrego labels
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Grafico aproximado de la funcion')
    #muestro el grafico
    plt.show()

def presentacion():
    print("\n\n")
    print("------------------------------------------------------------------------------")
    print ("Metodo Newton-Secante aproxima raices de funicones")
    print("------------------------------------------------------------------------------")
    print ("Integrantes: Alejo Menini, Juan Caceffo, Sol Lopez, Pablo Foglia")
    print("------------------------------------------------------------------------------")
    print("cursada: 2023 cuatrimestre 1")
    print("------------------------------------------------------------------------------")
    print("\n\n")

def printSteps(x1,pasos):
    print (f"\npaso : {pasos} -------- raizActual = {decimal_truncate(x1,RANGO_TOLERABLE.stop)} -------- f(raizActual) = {decimal_truncate(f(x1),RANGO_TOLERABLE.stop)}\n")

#x = valor inicial
#tolerancia = valor del intervalo como temrino de parada de convergencia
def newton(x,tolerancia):
    pasos = 0
    #anidamos funcion para poder utilizar variables no locales
    def secante():
        try:
            return x1 - ((f(x1)*(x1-x))/(f(x1)-f(x)))
        except ZeroDivisionError:
            print(f"error: f({x}) = 0, no se puede dividir por 0")
            exit(6)
    #------------------------- fin secante ----------------------------------    
    while(True):    
        try:
            x1 = x - (f(x)/f1(x))
        except ZeroDivisionError:
            print(f"error: f'({x}) = 0, no se puede dividir por 0")
            exit(6)
        if (abs(x-x1) <= tolerancia):
            break
        x = secante()
        pasos += 1 
        printSteps(x,pasos)
    return (x1)
    
def dataEntry():
    x = float(input("ingrese un numero del domino de x cercano a la raiz buscada: "))
    # Pedir al usuario la cantidad de decimales correctos
    #rango de exactitud de decimales posible
    global RANGO_TOLERABLE
    RANGO_TOLERABLE = range(1,11)
    exactitud = int(input(f"ingrese la cantidad de decimales correctos que desea, (deben estar dentro del rango ({RANGO_TOLERABLE.start}..{RANGO_TOLERABLE.stop-1}): "))
    #verificar que la exactitud ingresada por el usuario este detro del rango
    while (not(exactitud in RANGO_TOLERABLE)):    
        exactitud = int(input(f"ingrese la cantidad de decimales correctos que desea, (deben estar dentro del rango ({RANGO_TOLERABLE.start}..{RANGO_TOLERABLE.stop-1}): "))
    #scamos el valor de paradad dada la exactitud
    tolerancia = "0."
    #agregamos tantos 0 como exactitud indicada
    for i in range(exactitud): tolerancia += "0"
    #agregamos un uno para indicar que es una fraccion
    tolerancia += "1"
    #convertimos a flotante para poder operar
    tolerancia = float(tolerancia)

    return (x,tolerancia,exactitud)

def main():
    presentacion()
    (x,epsilon,exactitud)= dataEntry()
    raiz = newton(x,epsilon)
    print(f"raiz aproximada con una exactitud de {exactitud} decimales = {decimal_truncate(raiz,exactitud)}")
    print(f"funcion evaluada en raiz aproximada sin truncar resultado: f({decimal_truncate(raiz,exactitud)}) = {(f(round(raiz,exactitud)))}")
    grafico(x,raiz)
main()  