import argparse
import math

# --------------------------
# CONFIGURACIÓN DE ARGPARSE
# --------------------------
parser = argparse.ArgumentParser(
    description='Calculadora de línea de comandos que evalúa expresiones matemáticas completas.'
)

# Recibe una única cadena: la expresión matemática
parser.add_argument(
    'expresion',
    help='Expresión matemática a evaluar. Ejemplos: "2 + 3", "sqrt(16)", "2**3 + sin(pi/2)"'
)

args = parser.parse_args()

# ----------------------------
# ENTORNO SEGURO PARA eval()
# ----------------------------
entorno_seguro = {
    'sqrt': math.sqrt,
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'log': math.log,       
    'log10': math.log10,   
    'exp': math.exp,          
    'pow': math.pow,
    'abs': abs,
    'round': round,
    'pi': math.pi,
    'e': math.e,
    '__builtins__': {}    
}

# --------------------------
# EVALUACIÓN DE LA EXPRESIÓN
# --------------------------
try:
    resultado = eval(args.expresion, entorno_seguro)
    print(f"Resultado: {resultado}")
except Exception as e:
    print(f"❌ Error al evaluar la expresión: {e}")
