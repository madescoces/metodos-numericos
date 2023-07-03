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
    plt.figure(figsize=(14, 8))

    # Agregar un único eje al cual se le aplicará el gráfico
    ax = plt.subplot(1, 1, 1)
    DOMINIO = 1
    PUNTO_X_MAX =  max(puntos_x)
    PUNTO_X_MIN = min(puntos_x)

    #genero datos para el dominio de x
    x_values = np.arange(PUNTO_X_MIN-DOMINIO,PUNTO_X_MAX+DOMINIO,step=0.01)
    #genero datos para la imagen de y
    y_values = ([f(x) for x in x_values])

    ax.plot(x_values,y_values)
    # Agregar el eje de abscisas
    ax.axhline(y=0, color='black', linestyle='--')
    # Agregar el eje de ordenadas
    plt.axvline(x=0, color='black', linestyle='--')
    #agrego puntos calulados 
    ax.scatter(puntos_x,puntos_y,color='red')

    # Personalizar el gráfico
    ax.set_title(tituloGrafico)
    ax.set_xlabel("X")
    ax.set_ylabel("F(X)")
    ax.grid(True)

    # Mostrar el gráfico
    plt.tight_layout()
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

def aproximarRaiz(start, tolerancia, funcion):
    s = sp.symbols('x')
    x = start
    derivada = sp.lambdify(s,sp.diff(funcion(s)), modules=['numpy'])
        
    def secante():
        try:
            return x1 - ((funcion(x1)*(x1-x))/(funcion(x1)-funcion(x)))
        except ZeroDivisionError:
            print(f"error: f({x}) = 0, no se puede dividir por 0")
            exit(6)
    
    while(True):    
        try:
            x1 = x - (funcion(x)/derivada(x))
        except ZeroDivisionError:
            print(f"error: f'({x}) = 0, no se puede dividir por 0")
            exit(6)
        
        if (abs(x-x1) <= tolerancia):
            break
        x = secante()
    
    return round((x1), Presicion.presicionActual())

##Polinomio de larange
def lagrange_interpolation(points):
    n = len(points)
    polynomial = []
    for i in range(n):
        term = []
        numerator = []
        denominator = []
        for j in range(n):
            if i != j:
                numerator.append('(x - {})'.format(points[j][0]))
                denominator.append('({} - {})'.format(points[i][0], points[j][0]))
        term.append('*'.join(numerator))
        term.append('/'.join(denominator))
        polynomial.append('*'.join(term))
    polynomial = '+'.join(polynomial)
    polynomial = sp.expand(polynomial)
    
    return polynomial


def generar_funcion_lagrange(puntos):
    x = sp.symbols('x')
    n = len(puntos)
    resultado = 0

    for i in range(n):
        termino = puntos[i][1]
        for j in range(n):
            if j != i:
                termino *= (x - puntos[j][0]) / (puntos[i][0] - puntos[j][0])
        resultado += termino
    
    return resultado