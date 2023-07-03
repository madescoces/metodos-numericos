import sys
sys.path.append(r'D:\Usuario\Pablo\Escritorio\workspace\metodos_numericos')

from abc import ABC, abstractmethod
import sympy as sp
import pandas as pd
import numpy as np
import re
from modulos.precision import *

np.set_printoptions(suppress=True)

#Clase general regresiones lineal, cuadratica y exponencial
class Regresion:
    df = pd.DataFrame
    x = sp.symbols('x')                                          # Simbolo X para usar en las fórmulas
    n = 0   

    def __init__(self, df:pd.DataFrame) -> None:

        if df.shape[1] != 2:
            raise ValueError(f"Se esperaba una lista con dos columnas y se obtuvo una con {len(df.shape[1])}.")

        self.df = df                                            # Dataframe a global   
        self.n = df.shape[0]                                    # Cantidad de registros para usar en promedios

    def promediar(self, col):
        return np.mean(col)

    def prodXY(self):
        return self.x_col()*self.y_col()
            
    def x2(self):
        return self.x_col()**2

    def y2(self):
        return self.y_col()**2

    def x_col(self):
        return self.df.iloc[:,0]

    def y_col(self):
        return self.df.iloc[:,1]

    def denominador(self):
        den = self.promediar(self.x2())-self.promediar(self.x_col())**2
        self.validarDenominador(den)
        return den

    def obtenerEcuacionSimbolica():
        return None

    def obtenerEcuacion(self):
        return sp.lambdify(self.x,self.obtenerEcuacionSimbolica(), modules=['numpy'])

    def pearsonError(self, rounded=False):
        coef =  self.numeradorPearson()/self.denominadorPearson()
        self.validarPearson(coef)
        return round(coef, Presicion.presicionActual()) if rounded else coef

    def denominadorPearson(self):
        den = np.sqrt(self.promediar(self.x2())-self.promediar(self.x_col())**2)*np.sqrt(self.promediar(self.y2())-self.promediar(self.y_col())**2)
        self.validarDenominador(den)
        return den

    def numeradorPearson(self):
        return self.promediar(self.prodXY())-self.promediar(self.x_col())*self.promediar(self.y_col())
    
    def validarDenominador(self, num):
        if num == 0:
            raise ValueError(f"El denominador de la función para calcular m dio cero")
    
    def validarPearson(self, num):
        if not -1 <= num <= 1:
            raise ValueError(f"El coeficiente debería estar entre -1 y 1 pero resultó en {num}")

    def imprimirEcuacion(self):
        # Define el patrón regex para encontrar números en la ecuación
        pattern = r"[-+]?\d+\.\d+"

        # Encuentra todos los números en la ecuación usando el patrón regex
        numbers = re.findall(pattern, str(self.obtenerEcuacionSimbolica()))

        # Redondea cada número a 4 decimales y conviértelo a cadena
        rounded_numbers = [str(round(float(num), Presicion.presicionActual())) for num in numbers]
       
        # Reemplaza los números originales por los números redondeados en la ecuación
        return sp.sympify(re.sub(pattern, lambda m: rounded_numbers.pop(0), str(self.obtenerEcuacionSimbolica())))


#Clase para calcular el m y b de la recta para usar en regresión lineal
class RegresionLinear(Regresion):
            
    def __init__(self, df: pd.DataFrame) -> None:
        super().__init__(df)

    def numeradorA(self):
        return self.promediar(self.prodXY())-self.promediar(self.x_col())*self.promediar(self.y_col())
    
    def numeradorB(self):
        return self.promediar(self.x2())*self.promediar(self.y_col())-self.promediar(self.x_col())*self.promediar(self.prodXY())
    
    def calcularA(self, rounded=False):
        return round(self.numeradorA()/self.denominador(),Presicion.presicionActual()) if rounded else self.numeradorA()/self.denominador()

    def calcularB(self, rounded=False):
        return round(self.numeradorB()/self.denominador(),Presicion.presicionActual()) if rounded else self.numeradorB()/self.denominador()
                
    def obtenerEcuacionSimbolica(self):
        equation = self.calcularA()*self.x+self.calcularB()
        return equation
    
class RegresionCuadratica(RegresionLinear):
    def __init__(self, df: pd.DataFrame) -> None:
        super().__init__(df)
    
    def x_col(self):
        return np.log(super().x_col())

    def y_col(self):
        return np.log(super().y_col())

    def calcularB(self, rounded=False):
        temp = super().calcularB()
        return round(np.e**temp,Presicion.presicionActual()) if rounded else np.e**temp
        
    def obtenerEcuacionSimbolica(self):
        equation = self.calcularB()*self.x**self.calcularA()
        return equation

class RegresionExponencial(RegresionCuadratica):
    def __init__(self, df: pd.DataFrame) -> None:
        super().__init__(df)

    def x_col(self):
        return self.df.iloc[:,0]
        
    def obtenerEcuacionSimbolica(self):
        equation = self.calcularB()*sp.E**(self.calcularA()*self.x)
        return equation

# Interfaz
class MetodoAproximacion(ABC):

    def __init__(self, funcion, puntos:pd.Series):
        self.funcion = funcion
        self.puntos = puntos
        self.i = 0
        self.x = 0
                    
    def execute(self, x:int):        
        self.i = x
        self.x = self.puntos[x]
        return self._calcular()
    
    def get(self,index):
        return self.puntos[self.i+index]
                           
    @abstractmethod
    def _calcular(self):        
        pass

class Adelante(MetodoAproximacion):
    def _calcular(self):              
        x = self.x
        next = self.get(1)
        next2 = self.get(2)

        d1 = (self.funcion(next) - self.funcion(x) ) / abs(next - x)
        d2 = (self.funcion(next2) - 2*self.funcion(next) + self.funcion(x)) / abs(next2 - x)**2
        return (d1, d2)

class Atras(MetodoAproximacion):
    def _calcular(self):
        x = self.x
        prev = self.get(-1)
        prev2 = self.get(-2)

        d1 = (self.funcion(x) - self.funcion(prev)) / abs( x - prev)
        d2 = (self.funcion(x) - 2*self.funcion(prev) + self.funcion(prev2)) / abs(x - prev2)**2
        return (d1, d2)

class Central(MetodoAproximacion):
    def _calcular(self):
        x = self.x
        prev = self.get(-1)
        next = self.get(1)

        d1 = (self.funcion(next) - self.funcion(prev)) / abs(next - prev)
        d2 = (self.funcion(next) - 2*self.funcion(x) + self.funcion(prev)) / abs(next - prev)**2
        return (d1, d2)

class DiferenciasNumericas:
    def __init__(self, puntos:pd.Series, funcion:Regresion):
        self.last = puntos.index[-1]
        self.puntos = puntos
        self.funcion = funcion
        self.x = 0

    def calcular(self, x:int):
        self.x = x
        return self._usarMejorEstrategia()

    def prev(self):
        return 0 if self.x==0 else self.x-1
    
    def next(self):
        return self.last if self.x==self.last else self.x+1

    def _usarMejorEstrategia(self):
        match self.x:
            case 0:
                return self._execute(Adelante(self.funcion, self.puntos))
            case self.last:
                return self._execute(Atras(self.funcion, self.puntos))
            case _:
                return self._execute(Central(self.funcion, self.puntos))
        
    def _execute(self, tipoCalculo:MetodoAproximacion):
        return tipoCalculo.execute(self.x)

def calcularTiempoDuplicacion(eq:RegresionExponencial):
    doubling_time = np.log(2) / eq.calcularA()
    return round(doubling_time, Presicion.presicionActual())
    


        