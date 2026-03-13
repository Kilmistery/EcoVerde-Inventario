import tkinter as tk
from tkinter import ttk
import sqlite3

def ventana_clientes():

    ventana = tk.Toplevel()
    ventana.title("Clientes registrados")
    ventana.geometry("500x400")

    tabla = ttk.Treeview(ventana)

    tabla["columns"] = ("ID", "Nombre", "Telefono")

    tabla.column("#0", width=0, stretch=tk.NO)
    tabla.column("ID", anchor=tk.CENTER, width=50)
    tabla.column("Nombre", anchor=tk.W, width=200)
    tabla.column("Telefono", anchor=tk.CENTER, width=150)

    tabla.heading("#0", text="")
    tabla.heading("ID", text="ID")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Telefono", text="Telefono")

    tabla.pack(fill="both", expand=True)

    conexion = sqlite3.connect("EcoVerdeDB.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()

    for cliente in clientes:
        tabla.insert("", tk.END, values=cliente)

    conexion.close()