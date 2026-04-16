
import tkinter as tk
from tkinter import messagebox
from clientes.mostrar_clientes import ventana_clientes
from productos.modulo_productos import ventana_productos
from ventas.modulo_ventas import ventana_ventas
import sqlite3


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

# BOTONES DEL SISTEMA
btn_productos = tk.Button(ventana, text="Productos", width=20, command=ventana_productos)
btn_productos.pack(pady=5)

btn_clientes = tk.Button(ventana, text="Clientes", width=20, command=ventana_clientes)
btn_clientes.pack(pady=5)

btn_ventas = tk.Button(ventana, text="Ventas", width=20, command=ventana_ventas)
btn_ventas.pack(pady=5)

btn_consignacion = tk.Button(ventana, text="Consignacion", width=20)
btn_consignacion.pack(pady=5)

btn_excel = tk.Button(ventana, text="Exportar a Excel", width=20)
btn_excel.pack(pady=5)


ventana.mainloop()