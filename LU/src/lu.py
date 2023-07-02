import numpy as np
import sympy as sp
import os
import random
from helper import *

#Setteo la impresion de matrices con 2 decimales
sp.init_printing(precision=2, use_unicode=True)

def wait():
    input("\n\nPresione cualquier tecla para continuar...")

def pmatrix(matriz):
    #Setteo la impresion de matrices con 2 decimales
    sp.init_printing(precision=2, use_unicode=True)
    sp.pprint(sp.Matrix(matriz).applyfunc(lambda x: round(x, 2)))

def presentacion():

    prLn(WIDTH,up=1,dw=1,lf=True)
    prTxt("                                                               ",lf=True,col=3,dw=1)
    prTxt("Descomposicion LU para matrices cuadradas NxN",lf=True,col=3,dw=1)
    prTxt("                                                               ",lf=True,col=3,dw=1)
    prTxt("Integrantes: Sol Lopez, Pablo Foglia, Juan Caceffo, Alejo Menini",lf=True,col=3,dw=1)
    prTxt("                                                               ",lf=True,col=3)
    prLn(WIDTH,up=1,dw=1,lf=True)

def det(matriz):
    filas, columnas = matriz.shape
    determinantes = []
    if filas != columnas:
        raise ValueError(" !!!! La matriz debe ser cuadrada para calcular las submatrices !!!! ")

    for i in range(2, filas+1):
        submatriz = matriz[:i, :i]
        print("\nSubmatriz %d\n"%(i-1))
        pmatrix(submatriz)
        determinante = np.linalg.det(submatriz)
        print("\nDeterminante: %.2f"%determinante)
        determinantes.append(determinante)

    for det in determinantes:
        if det == 0:
            raise ValueError(" !!!! La matriz tiene una determinante en 0 por lo que no se puede utilizar LU !!!! ")
    print("\n*** Al ser todas las determinantes distintas de cero procedemos a realizar LU ***")

def rand():
    return round(random.uniform(-100,100),2)

def validateInput():
    rta = input("Respuesta: ")
    count = 0
    while rta.lower() != 's' and rta.lower() != 'n':
        if count==3:
            print("En serio hace falta que te lo vuelva a preguntar?")
        if count==4:
            print("No es muy dificil... Ingresa S o N...Dale...")
        if count==5:
            print("No era tan difil tu task... Chau")
            exit()
        rta = input("Respuesta ingresada no valida, volver a intentar: ")
        count+=1
    
    return rta

def generadorMatrix():
    print("\nGenerar alreatoriamente la matriz?\nS - Genera una matriz random\nN - Debera ingresar todos los valores a mano")
    rta = validateInput()
    
    print("\nGeneramos la matriz A\n")
    for r in range (0,n):
        for c in range(0,n):
            matriz[r,c] = rand() if (rta == 's') else input("El elemento a["+str(r+1)+","+str(c+1)+"]: ")
            matriz[r,c] = float(matriz[r,c])
            mockMatriz[r,c] = float(matriz[r,c])
            u[r,c] = matriz[r,c]
    
    print("\nGeneramos la matriz B\n")
    for r in range (0,n):
        b[r,0] = rand() if (rta == 's') else input("El elemento b["+str(r+1)+","+str(c+1)+"]: ")

    wait()

    cls()
    print("\nEsta es la matriz A con la que vamos a trabajar...\n")
    pmatrix(matriz)

    print("\nEsta es la matriz B con la que vamos a trabajar...\n")
    pmatrix(b)

    wait()

########################### MAIN #####################################

cls()
presentacion()
n = int(input("\n\nIngrese la dimension NxN de la matriz cuadrada: "))
matriz = np.zeros([n,n])
mockMatriz = np.zeros([n,n])
b = np.zeros([n,1])
l = np.zeros([n,n])
u = np.zeros([n,n])

generadorMatrix()

cls()
print("\nCalculamos todas las determinantes de las matrices principales...")
det(matriz)
wait()

for k in range(0,n):
    for r in range(0,n):
        if (k==r):
            l[k,r] = 1
        if (k<r):
            factor = (mockMatriz[r,k]/mockMatriz[k,k])
            l[r,k] = factor
            for c in range(0,n):
                mockMatriz[r,c] = mockMatriz[r,c]-(factor*mockMatriz[k,c])
                u[r,c] = mockMatriz[r,c]

cls()
print("\nNuestra matriz L queda asi...\n")
pmatrix(l)
print("\nNuestra matriz U queda asi...\n")
pmatrix(u)
wait()

#Ly=b
cls()
print("\nObtenidas nuestras matrices L y U procedemos a calcular *LY = b*")
print("Despejaremos *Y* para que nos quede la siguiente ecuacion...")
print("Y = b/L --> Y = b * L^(-1)")

print("\nCalculamos la inversa de L...")
linv = np.linalg.inv(l)
pmatrix(linv)

print("\nMultiplicamos b y L^(-1) para obtener *Y*")
valores_y = np.matmul(linv, b)
print("\nMatriz Y")
pmatrix(valores_y)
wait()

#Ux=y
cls()
print("\nObtenidos los valores de Y procedemos a calcular *UX = Y*")
print("Despejaremos *X* para que nos quede la siguiente ecuacion...")
print("X = Y/U --> X = Y * U^(-1)")

print("\nCalculamos la inversa de U...")
uinv = np.linalg.inv(u)
pmatrix(uinv)

print("\nMultiplicamos Y y U^(-1) para obtener *X*")
valores_x = np.matmul(uinv, valores_y)
print("\nMatriz X")
pmatrix(valores_x)
wait()

#Ax = b
cls()
print("\nEncontrados los valores de X corroboramos que sean correctos haciendo la cuenta original *AX = b*")
bEncontrados = np.matmul(matriz, valores_x)
print("\nValores de B con nuestros X encotrados")
pmatrix(bEncontrados)
print("\nValores de B originales")
pmatrix(b)
wait()

cls()
print("\nGracias por usar nuestro sistema!!!\nAdios")