# Importamos libreria numpy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import os

def limpiarConsola():
    #limpiar consola en Linux
    if (os.name == "posix"):
        os.system("clear")
    elif (os.name == "nt"):
        #limpar consola en windows
        os.system("cls")

def presentacion():
    print("\n\n")
    print("------------------------------------------------------------------------------")
    print ("Metodo Jacobi que resuelve ecuaciones lineales con una matriz de N X N")
    print("------------------------------------------------------------------------------")
    print ("Integrantes: Alejo Menini, Juan Caceffo, Sol Lopez, Pablo Foglia")
    print("------------------------------------------------------------------------------")
    print("\n\n")


def datosJacobi():
    # Pedir al usuario la dimensión del sistema de ecuaciones
    n = int(input("Ingrese la dimensión del sistema de ecuaciones: "))

    # Pedir al usuario los elementos de la matriz A
    print("Ingrese la matriz A:")
    A = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            A[i, j] = float(input(f"Ingrese el elemento A[{i}][{j}]: "))
    
    
    while not validarMatriz(A):
        print("\nLa matriz ingresada no cumple con las exigencias del algoritmo de Jacobi.")
        print("Por favor, ingrese una matriz que sea diagonal dominante y no singular.")
        print("Ingrese la matriz A:")
        A = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                A[i, j] = float(input(f"Ingrese el elemento A[{i}][{j}]: "))
    
    print("Esto es la matriz A")
    print(A)        

    # Pedir al usuario los elementos del vector B
    print("\nIngrese la matirz B:")
    B = np.zeros(n)
    for i in range(n):
        B[i] = float(input(f"Ingrese el elemento b[{i}]: "))

    print("\nEste es el vector B")
    print(B)
    # Valores iniciales para el metodo
    x0 = np.zeros_like(B)


    # Pedir al usuario la cantidad de decimales correctos
    #rango de exactitud de decimales posible
    RANGO_TOLERABLE = range(1,11)
    exactitud = int(input(f"ingrese la cantidad de decimales correctos que desea, (debe estar dentro del rango ({RANGO_TOLERABLE.start}..{RANGO_TOLERABLE.stop-1}): "))
    #verificar que la exactitud ingresada por el usuario sea correcta 
    while (not(exactitud in RANGO_TOLERABLE)):    
        exactitud = int(input(f"ingrese la cantidad de decimales correctos que desea, (debe estar dentro del rango ({RANGO_TOLERABLE.start}..{RANGO_TOLERABLE.stop-1}): "))
    #scamos el valor de paradad dada la exactitud
    tolerancia = "0."
    #agregamos tantos 0 como exactitud indicada
    for i in range(exactitud): tolerancia += "0"
    #agregamos un uno para indicar que es una fraccion
    tolerancia += "1"
    #convertimos a flotante para poder operar
    tolerancia = float(tolerancia)

    return (A,B,x0,tolerancia,exactitud)
    
def validarMatriz(A):
    n = A.shape[0]
    
    # Verificar matriz diagonal dominante
    for i in range(n):
        row_sum = np.sum(np.abs(A[i, :])) - np.abs(A[i, i])
        if np.abs(A[i, i]) <= row_sum:
            return False
    
    # Verificar matriz no singular
    if np.linalg.det(A) == 0:
        return False
    
    return True

def truncar_array(array, decimales):
    factor = np.power(10, decimales)
    return np.floor(array * factor) / factor


# A = matriz, B = vector independiente x0 = vector inicial para el metodo de Jacobi
# tol = tolerancia para determinar convergencia de metodo
#exactitud = cantidad de decimales correctos
# max_iter = Número máximo de iteraciones permitidas 
def jacobi(A, B, x0, tol, exactitud,max_iter=100):
    # Se determina el tamaño del vector para que este sea recorrido en el ciclo for
    n = len(B)
    # Se copia el vector para asi poder mantener el vector inicial sin modificar en el proceso iterativo
    x = x0.copy()
    x_copy = np.zeros_like(x)
    convergence = []  

    for iteracion in range(max_iter):
        for i in range(n):

            sum_term = 0
            for j in range(n):
                if j != i:
                    sum_term += A[i, j] * x[j]
            # Se calcula el nuevo valor de la variable dividiendo la diferencia entre b[i] (el término independiente) y sum_term entre A[i, i] (el coeficiente diagonal)
            x_copy[i] = (B[i] - sum_term) / A[i, i]
            convergence.append(x_copy.copy())  
        print(f"\npaso {iteracion+1} -------------- aproximacion actual = {truncar_array(x_copy,exactitud)}")

        # Se calcula la norma del vector de corrección x_new - x. Si esta norma es menor que la tolerancia, se considera que el método ha convergido
        # caso contrario devuelve el mensaje
        if np.linalg.norm(x_copy - x) < tol:
            return x_copy,(iteracion+1),convergence
        
        x = x_copy.copy()

    print("El método de Jacobi no converge después de", max_iter, "iteraciones.")
    return x,(iteracion+1),convergence

def solucionExacta(A,B):
    solution = np.linalg.solve(A, B)
    return solution


def graficarConvergencia(convergencia_y,x_values):
    for approx in convergencia_y:
        plt.scatter(x_values, approx,c="red")
    #grafico aproximacion final
    aproxFinal = convergencia_y[-1]
    plt.scatter(x_values, aproxFinal,c="blue")
    plt.xlabel("Componentes del vector")
    plt.ylabel("Aproximación")
    plt.title("Convergencia del método de Jacobi")
    #configuracion de la leyenda
    config_intermedias = Patch(color='red', label='Aproximaciones intermedias')
    config_final = Patch(color='blue', label='Aproximación final')
    # Agregar leyendas personalizadas
    plt.legend(handles=[config_intermedias, config_final])
    plt.grid(True)
    plt.show()


def main():
    presentacion()
    DATE = datosJacobi()
    limpiarConsola()
    presentacion()
    solution_jacobi, num_iterations, convergencia = jacobi(*DATE)
    solution_exacta = solucionExacta(*DATE[:2])
    ##truncando solucion jacobi
    EXACTITUD = DATE[4]
    solution_jacobi = truncar_array(solution_jacobi,EXACTITUD) 

    print("\n\nSolucion exacta utilizando metodo distinto:")
    print(solution_exacta)
    # Imprimimos por pantalla la solucion
    print("Para el sistema de ecuaciones lineal:\n")
    X = [f"x{i}" for i in range(DATE[1].shape[0])]
    print (DATE[0],"*",np.array(X),"=",DATE[1],"\n")
    print("La solucion aproximada con metodo Jacobi es:")
    print(np.array(X),":",solution_jacobi)
    print("Número de iteraciones:", num_iterations)

    graficarConvergencia(convergencia,X)    
   
        
main()