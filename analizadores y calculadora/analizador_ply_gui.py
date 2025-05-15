# analizador_ply_gui.py
import tkinter as tk
from tkinter import messagebox
import ply.lex as lex #análisis léxico 
import ply.yacc as yacc #análisis sintáctico

# Lexer
tokens = ('NUM', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN')
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t\n'
def t_error(t):
    raise SyntaxError(f"Carácter ilegal: {t.value[0]}")

lexer = lex.lex()

# Parser
def p_expr_bin(p):
    '''expr : expr PLUS term
            | expr MINUS term'''
    p[0] = p[1] + p[3] if p[2] == '+' else p[1] - p[3]

def p_expr_term(p):
    'expr : term'
    p[0] = p[1]

def p_term_bin(p):
    '''term : term TIMES factor
            | term DIVIDE factor'''
    p[0] = p[1] * p[3] if p[2] == '*' else p[1] / p[3]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_num(p):
    'factor : NUM'
    p[0] = p[1]

def p_factor_expr(p):
    'factor : LPAREN expr RPAREN'
    p[0] = p[2]

def p_error(p):
    raise SyntaxError("Error de sintaxis")

parser = yacc.yacc()

def evaluar():
    entrada = entry_expr.get()
    try:
        resultado = parser.parse(entrada)
        lbl_resultado.config(text=f"Resultado: {resultado}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI
ventana = tk.Tk()
ventana.title("Analizador PLY")

tk.Label(ventana, text="Expresión matemática:").pack()
entry_expr = tk.Entry(ventana, width=40)
entry_expr.pack()

tk.Button(ventana, text="Evaluar", command=evaluar).pack(pady=5)
lbl_resultado = tk.Label(ventana, text="Resultado:")
lbl_resultado.pack(pady=10)

ventana.mainloop()
