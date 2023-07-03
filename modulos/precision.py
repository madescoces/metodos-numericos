import re
import numpy as np

class Presicion:
    PRECISION = 2

    @classmethod
    def cambiarPresicionRepresentacion(cls, errorTolerado: float):
        cls.validarFlotante(errorTolerado)
        cls.validarFormatoError(errorTolerado)
        cls.PRECISION = cls.digitosDePresicion(errorTolerado)

    @classmethod
    def digitosDePresicion(cls, valor) -> int:
        valorTXT = cls.decimalASTR(valor)
        return len(valorTXT.split('.')[-1])

    @classmethod
    def presicionActual(cls) -> int:
        return cls.PRECISION

    @staticmethod
    def validarFlotante(numero):
        try:
            float(numero)
        except:
            raise TypeError(f"Se esperaba float y se obtuvo {type(numero).__name__}.")
    
    @classmethod
    def validarFormatoError(cls, numero):
        patron = r"^(0\.0+1|0\.1)$"        
        if not bool(re.match(patron, cls.decimalASTR(numero))):
            raise ValueError(f"Se esperaba un número del tipo 0.01 y se obtuvo {numero}.")
    
    @staticmethod
    def decimalASTR(numero):
        decimales = abs(int(np.log10(numero)))
        return '{:.{}f}'.format(numero, decimales)

    @classmethod
    def presicionActualEnDecimal(cls) -> float:
        precision = 10 ** (Presicion.presicionActual())
        resultado = 1 / precision
        return resultado