import os
import math

SYMBOL = '█'#'♡'#'✧ '#'█░'
WIDTH = int(100/len(SYMBOL))
LEFTMARGIN = 2

def cls():
    # Verificar el sistema operativo y ejecutar el comando correspondiente para limpiar la pantalla
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Unix/Linux/Mac
        os.system('clear')

def _prLn(size, **kwargs):
    up = int(kwargs['up']) if 'up' in kwargs else 0
    dw = int(kwargs['dw']) if 'dw' in kwargs else 0
    lf = bool(kwargs['lf']) if 'lf' in kwargs else False
    
    for _ in range(up):
        print("\n", end="")
    _lftMg() if lf else ""
    for _ in range(size):
        print(f"{SYMBOL}", end="")
    for _ in range(dw):
        print("\n", end="")

def _prTxt(txt, **kwargs):
    up = int(kwargs['up']) if 'up' in kwargs else 0
    dw = int(kwargs['dw']) if 'dw' in kwargs else 0
    lf = bool(kwargs['lf']) if 'lf' in kwargs else False
    col = int(kwargs['col']) if 'col' in kwargs else 3
    
    c1 = WIDTH*len(SYMBOL)
    c2 = len(txt)
    c3 = len(SYMBOL)*col*2
    free =  c1 - c2 - c3
    left = math.floor(free/2)
    right = left if (free%2 == 0) else left+1
    txt_spaced = _prSpc(left) + txt + _prSpc(right)
   
    for _ in range(up):
        print("\n", end="")
    _prLn(col,lf=lf)
    print(f"{txt_spaced}", end="")
    _prLn(col) 
    for _ in range(dw):
        print("\n", end="")  

def _lftMg():
    for _ in range(LEFTMARGIN):
        print("\t", end="")

def _prSpc(size) -> str:
    whiteSpace = ""
    for _ in range(size):
        whiteSpace += " "
    return whiteSpace

def menu(title:str):
    _prLn(WIDTH,up=1,dw=1,lf=True)
    _prTxt("                                                               ",lf=True,col=3,dw=1)
    _prTxt(title,lf=True,col=3,dw=1)
    _prTxt("                                                               ",lf=True,col=3,dw=1)
    _prTxt("Integrantes: Sol Lopez, Pablo Foglia, Juan Caceffo, Alejo Menini",lf=True,col=3,dw=1)
    _prTxt("                                                               ",lf=True,col=3)
    _prLn(WIDTH,up=1,dw=1,lf=True)
    print("\n\n")
