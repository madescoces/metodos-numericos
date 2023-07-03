import sys
sys.path.append(r'D:\Usuario\Pablo\Escritorio\workspace\metodos_numericos')

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import re
from modulos.precision import *

#puntos = puntos a  grafifcar
#f = funcion a graficar 
def graficar(puntos_x,puntos_y,f,tituloGrafico:str):
    PUNTO_X_MAX =  max(puntos_x)
    PUNTO_X_MIN = min(puntos_x)
    DOMINIO = 5
    #genero datos para el dominio de x
    x_values = np.arange(PUNTO_X_MIN-DOMINIO,DOMINIO+PUNTO_X_MAX,step=0.01)
    #genero datos para la imagen de y
    y_values = ([f(x) for x in x_values])
    #ploteo el grafico
    plt.plot(x_values,y_values)
    # Agregar el eje de abscisas
    plt.axhline(y=0, color='black', linestyle='--')
    # Agregar el eje de ordenadas
    plt.axvline(x=0, color='black', linestyle='--')
    #agrego puntos calulados 
    plt.scatter(puntos_x,puntos_y,c="red")
    #agrego labels
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title(tituloGrafico)
    PUNTOS_Y_MIN = min(puntos_y)
    PUNTOS_Y_MAX = max(puntos_y)
    plt.ylim(PUNTOS_Y_MIN-DOMINIO,PUNTOS_Y_MAX+DOMINIO)
    #muestro el grafico
    plt.show()


def productoria(points, step, txt=False, **kwargs):
    x =  kwargs['x'] if 'x' in kwargs else points[step][0]
    evaluado = 1
    noEvaluado = ""
    for i in range(step):
        noEvaluado += f'*(x - ({points[i][0]}))'
        evaluado *= (x - (points[i][0]))
    return evaluado if not txt else noEvaluado   

def alphas(points:list):
    alphaList = [] 
    
    def prevAlphas(p):
        acum = 0
        for i in range(len(alphaList)):
            acum += alphaList[i] if i < 1 else alphaList[i]*productoria(points,i,x=p)
        return acum

    for i,p in enumerate(points):           
        alpha = (points[i][1]-(prevAlphas(p[0]) if i>0 else 0))/productoria(points, i) 
        alphaList.append(alpha)
       
    return alphaList

def validarNum(txt:str, nat=False, **kwargs):
    min =  kwargs['min'] if 'min' in kwargs else None
    while True:
        val = input(txt)  
        try:
            val = float(val)
            if val.is_integer():
                val = int(val)
            if (min and val < min):
                raise Exception(f"Error: El número debe ser mayor de {min}") 
            if (nat and (val <= 0)):
                raise Exception("Error: Se esperaba un número mayor a 0")                
            return val
        except ValueError:
            print("Error: Se esperaba un valor numérico válido.") 
        except Exception as e:
            print(e)      

def choice(txt:str):
    ch = str(input(txt))
    while(ch.lower() != 's' and ch.lower() != 'n'):
        print(f'Se esperaba S/N pero se obtubo {ch}.')
        ch = str(input(txt))
    return True if ch.lower() == 's' else False

def saltosDeLinea(cantSaltos):
    for i in range(cantSaltos): print("\n")

def generacionPuntosAleatorios(cantPuntos):
    puntos_x = np.random.choice(np.round(np.random.uniform(-10, 30, size=cantPuntos),3), size=cantPuntos, replace=False)
    puntos_y = np.random.choice(np.round(np.random.uniform(-20, 40, size=cantPuntos),3), size=cantPuntos, replace=False)
    return [(x,y) for x,y in zip(puntos_x, puntos_y)]

class NEquation:
    def __init__(self, points, **kwargs) -> None:
        self.pn =  kwargs['pn'] if 'pn' in kwargs else len(points)    
        self.points = points
        self.x = sp.symbols('x')
        
    def obtenerEcuacionSimbolica(self):        
        alphaList = alphas(self.points)
        equation = f'{alphaList[0]}'

        for i in range(self.pn):
            if i > 0:
                equation += f'{"+" if alphaList[i] > 0 else ""}{round(alphaList[i],Presicion.presicionActual())}{productoria(self.points,i,True)}'
        
        return equation

    def equation(self):
        equation = self.obtenerEcuacionSimbolica()
        return sp.lambdify(self.x, equation, modules=['numpy'])

    def imprimirEcuacion(self):
        return sp.sympify(self.obtenerEcuacionSimbolica())

class Puntos:
    def __init__(self, manualStep=False):
        self.steps = int(validarNum('Ingrese la cantidad de puntos:',True)) if manualStep else 20
        self.XN = np.array([])
        self.YN = np.array([])
    
    def generar(self):
        for i in range(self.steps):
            self.XN = np.append(self.XN, validarNum(f'Ingrese el valor para X{i}'))
            self.YN = np.append(self.YN, validarNum(f'Ingrese el valor para Y{i}'))

    def obtenerPuntos(self):
        self.generar()
        return [(x,y) for x,y in zip(self.XN, self.YN)]

class PuntosAleatorios(Puntos):
    def __init__(self, X_Equal_Y, manualStep=False):
        Puntos.__init__(self, manualStep)   
        self.x_min = validarNum('Ingrese la cota menor para x:')
        self.x_max = validarNum('Ingrese la cota mayor para x:',min=self.x_min)
        self.y_min = self.x_min
        self.y_max = self.x_max
        if not X_Equal_Y:
            self.y_min = validarNum('Ingrese la cota inferior para y:')
            self.y_max = validarNum('Ingrese la cota superior para y:',min=self.y_min)
        
    def generar(self):
        #Genera arrays con numeros aleatorios y diferentes entre si
        self.YN = np.random.choice(np.round(np.random.uniform(self.y_min, self.y_max, size = self.steps),3), size=self.steps, replace=False)
        self.XN = np.random.choice(np.round(np.random.uniform(self.x_min, self.x_max, size = self.steps),3), size=self.steps, replace=False)


def testeoGrado(puntos, funcion):
    grado_teorico = len(puntos) - 1
    grado_obtenido = sp.degree(funcion)

    if (grado_teorico != grado_obtenido):
        raise Exception(f'Error: el grado del polinomio obtenido fue {grado_obtenido} y se esperaba {grado_teorico}.')
    
    return grado_obtenido