import sqlite3
import tkinter as tk
from tkinter import messagebox

# Crear base de datos
conexion = sqlite3.connect("EcoVerdeDB.db")
cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS productos (
id INTEGER PRIMARY KEY AUTOINCREMENT,
nombre TEXT,
precio REAL,
stock REAL)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
id INTEGER PRIMARY KEY AUTOINCREMENT,
nombre TEXT,
telefono TEXT)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS ventas (
id INTEGER PRIMARY KEY AUTOINCREMENT,
cliente_id INTEGER,
producto_id INTEGER,
cantidad INTEGER,
total REAL,
fecha TEXT)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS consignaciones (
id INTEGER PRIMARY KEY AUTOINCREMENT,
cliente_id INTEGER,
producto_id INTEGER,
cantidad INTEGER,
estado TEXT)
""")

conexion.commit()
conexion.close()

print("Base de datos creada correctamente")


# Crear ventana principal
ventana = tk.Tk()
ventana.title("Sistema EcoVerde - Inventario")
ventana.geometry("400x400")

titulo = tk.Label(ventana, text="Sistema EcoVerde", font=("Times New Roman", 16))
titulo.pack(pady=20)


# FUNCION PRODUCTOS
def abrir_productos():

    ventana_productos = tk.Toplevel(ventana)
    ventana_productos.title("Productos")
    ventana_productos.geometry("300x300")

    tk.Label(ventana_productos, text="Nombre").pack()
    entry_nombre = tk.Entry(ventana_productos)
    entry_nombre.pack()

    tk.Label(ventana_productos, text="Precio").pack()
    entry_precio = tk.Entry(ventana_productos)
    entry_precio.pack()

    tk.Label(ventana_productos, text="Stock").pack()
    entry_stock = tk.Entry(ventana_productos)
    entry_stock.pack()


    def guardar_producto():

        nombre = entry_nombre.get()
        precio = entry_precio.get()
        stock = entry_stock.get()

        conexion = sqlite3.connect("EcoVerdeDB.db")
        cursor = conexion.cursor()

        cursor.execute(
            "INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
            (nombre, precio, stock)
        )

        conexion.commit()
        conexion.close()

        messagebox.showinfo("EcoVerde", "Producto guardado correctamente")


    btn_guardar = tk.Button(
        ventana_productos,
        text="Guardar producto",
        command=guardar_producto
    )

    btn_guardar.pack(pady=10)


# BOTONES DEL SISTEMA
btn_productos = tk.Button(ventana, text="Productos", width=20, command=abrir_productos)
btn_productos.pack(pady=5)

btn_clientes = tk.Button(ventana, text="Clientes", width=20)
btn_clientes.pack(pady=5)

btn_ventas = tk.Button(ventana, text="Ventas", width=20)
btn_ventas.pack(pady=5)

btn_consignacion = tk.Button(ventana, text="Consignacion", width=20)
btn_consignacion.pack(pady=5)

btn_excel = tk.Button(ventana, text="Exportar a Excel", width=20)
btn_excel.pack(pady=5)


ventana.mainloop()