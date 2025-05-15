import tkinter as tk
from tkinter import messagebox
import ast
import astpretty

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def eat(self, expected):
        if self.current_token() == expected:
            self.pos += 1
        else:
            raise SyntaxError(f"Esperado {expected}, pero encontrado {self.current_token()}")

    def parse(self):
        return self.expr()

    def expr(self):
        node = self.term()
        while self.current_token() in ('+', '-'):
            op = self.current_token()
            self.eat(op)
            node = ast.BinOp(left=node, op=ast.Add() if op == '+' else ast.Sub(), right=self.term())
        return node

    def term(self):
        node = self.factor()
        while self.current_token() in ('*', '/'):
            op = self.current_token()
            self.eat(op)
            node = ast.BinOp(left=node, op=ast.Mult() if op == '*' else ast.Div(), right=self.factor())
        return node

    def factor(self):
        token = self.current_token()
        if token.isdigit():
            self.eat(token)
            return ast.Constant(value=int(token))
        elif token == '(':
            self.eat('(')
            node = self.expr()
            self.eat(')')
            return node
        else:
            raise SyntaxError("Token inválido")

def tokenize(expr):
    return [t for t in expr if t.strip()]

# -------------------------
# Dibujar árbol en Canvas
# -------------------------
def dibujar_arbol(canvas, nodo, x, y, nivel=0, padre_coords=None):
    radio = 30
    espaciado_x = 80
    espaciado_y = 80

    etiqueta = type(nodo).__name__
    if isinstance(nodo, ast.Constant):
        etiqueta += f"\n{nodo.value}"

    # Dibujar nodo actual
    canvas.create_oval(x - radio, y - radio, x + radio, y + radio, fill="lightgray")
    canvas.create_text(x, y, text=etiqueta, font=("Arial", 10), justify="center")

    if padre_coords:
        canvas.create_line(padre_coords[0], padre_coords[1] + radio, x, y - radio)

    # Dibujar hijos en orden explícito si es BinOp
    hijos = []
    if isinstance(nodo, ast.BinOp):
        hijos.append(nodo.left)
        hijos.append(nodo.op)
        hijos.append(nodo.right)
    else:
        for _, valor in ast.iter_fields(nodo):
            if isinstance(valor, ast.AST):
                hijos.append(valor)
            elif isinstance(valor, list):
                for item in valor:
                    if isinstance(item, ast.AST):
                        hijos.append(item)


    n = len(hijos)
    inicio_x = x - (n - 1) * espaciado_x // 2
    for i, hijo in enumerate(hijos):
        nuevo_x = inicio_x + i * espaciado_x
        dibujar_arbol(canvas, hijo, nuevo_x, y + espaciado_y, nivel + 1, (x, y))

# -------------------------
# Mostrar texto + visual
# -------------------------
def mostrar_arbol():
    entrada_expr = entry.get().replace(" ", "")
    try:
        tokens = tokenize(entrada_expr)
        parser = Parser(tokens)
        tree = parser.parse()
        tree = ast.fix_missing_locations(tree)

        # Mostrar AST como texto
        output.delete("1.0", tk.END)
        output.insert(tk.END, astpretty.pformat(tree))

        # Mostrar AST como dibujo
        mostrar_en_canvas(tree)

    except Exception as e:
        messagebox.showerror("Error", str(e))

def mostrar_en_canvas(tree):
    ventana_canvas = tk.Toplevel()
    ventana_canvas.title("Árbol Visual en Canvas")

    canvas = tk.Canvas(ventana_canvas, width=1000, height=600, bg="white", scrollregion=(0, 0, 2000, 1000))
    canvas.pack(fill="both", expand=True)

    # Barras de desplazamiento
    x_scroll = tk.Scrollbar(ventana_canvas, orient="horizontal", command=canvas.xview)
    y_scroll = tk.Scrollbar(ventana_canvas, orient="vertical", command=canvas.yview)
    canvas.config(xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set)

    x_scroll.pack(side="bottom", fill="x")
    y_scroll.pack(side="right", fill="y")

    # Dibujar árbol
    dibujar_arbol(canvas, tree, x=500, y=60)

# -------------------------
# INTERFAZ PRINCIPAL
# -------------------------
ventana = tk.Tk()
ventana.title("Analizador Descendente Recursivo")

tk.Label(ventana, text="Expresión:").pack()
entry = tk.Entry(ventana, width=30)
entry.pack()

tk.Button(ventana, text="Construir AST", command=mostrar_arbol).pack(pady=5)

output = tk.Text(ventana, height=20, width=60)
output.pack()

ventana.mainloop()
