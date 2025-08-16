import tkinter as tk
from tkinter import simpledialog, messagebox

root = tk.Tk()
root.withdraw()  #este comando oculta ventana principal, si no lo ponemos 
                   #se nos hace una ventana grande al lado

#el simpledialog es un modulo de la libreria tkinter usado para dialogos
num1 = simpledialog.askfloat("Suma", "Ingrese el primer número:")
num2 = simpledialog.askfloat("Suma", "Ingrese el segundo número:")

if num1 is not None and num2 is not None:
    resultado = num1 + num2
    messagebox.showinfo("Resultado", f"La suma es: {resultado}")
else:
    messagebox.showwarning("Cancelado", "No ingresaste ambos números.")
    