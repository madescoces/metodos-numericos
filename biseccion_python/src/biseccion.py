from math import *

def f(x):
    return e**-x -sin(x)

def puntoMedio(a,b):
    return (a + b)/2

def calculoError(a,b):
    return (b-a)/2

def biseccion(puntoA,puntoB,tolerancia):
    a = puntoA
    b = puntoB
    i = 0
    e = calculoError(a,b)

    if (f(a)*f(b)>0):
            print(f"No existen raices entre {a} y {b} o puede haber más de una raiz")            
    else:   
        while( e > tolerancia ):            
            i += 1
            m = puntoMedio(a,b)
            if (m==0):            
                break            
            if (f(a)*f(m) < 0):
                b = m                
            elif (f(b)*f(m) < 0):
                a = m
  
            e = calculoError(a,b)
            
        print(f"Se halló la raiz en {m}")    
        print(f"El programa iteró {i} veces")    
        return m

biseccion(8,10,0.001)

