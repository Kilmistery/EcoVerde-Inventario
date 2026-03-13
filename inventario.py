import sqlite3

conexion = sqlite3.connect("EcoVerdeDB.db")
cursor = conexion.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS productos (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, precio REAL, stock REAL)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS clientes (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, telefono TEXT)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS ventas (id INTEGER PRIMARY KEY AUTOINCREMENT, cliente_id INTEGER, producto_id INTEGER, cantidad INTEGER, total REAL, fecha TEXT)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS consignaciones (id INTEGER PRIMARY KEY AUTOINCREMENT, cliente_id INTEGER, producto_id INTEGER, cantidad INTEGER, estado TEXT)""")

conexion.commit()
conexion.close()

print("Base de datos creada correctamente")


import tkinter as tk

#Crear Ventana principal
ventana = tk.Tk()
ventana.title("Sistema EcoVerde - Inventario")
ventana.geometry("400x400")

titulo = tk.Label(ventana, text="Sistema EcoVerde", font=("Times New Roman", 16))
titulo.pack(pady=20)

#Botones del sistema
btn_productos = tk.Button(ventana, text="Productos", width=20)
btn_productos.pack(pady=5)

btn_clientes = tk.Button(ventana, text="Clientes", width=20)
btn_clientes.pack(pady=5)

btn_ventas = tk.Button(ventana, text="Ventas", width=20)
btn_ventas.pack(pady=5)

btn_consignacion = tk.Button(ventana, text="Consignacion", width=20)
btn_consignacion.pack(pady=5)

btn_excel = tk.Button(ventana, text="Exportar a Excel", width=20)
btn_excel.pack(pady=5)

#Iniciar programa
ventana.mainloop()