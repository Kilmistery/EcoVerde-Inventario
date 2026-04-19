import tkinter as tk
from tkinter import ttk
import sqlite3

def ventana_mostrar_ventas():

    ventana = tk.Toplevel()
    ventana.title("Historial de Ventas")
    ventana.geometry("800x400")

    # TABLA
    tabla = ttk.Treeview(ventana)

    tabla["columns"] = ("ID", "Cliente", "Producto", "Cantidad", "Total", "Fecha")

    tabla.column("#0", width=0, stretch=tk.NO)
    tabla.column("ID", anchor=tk.CENTER, width=50)
    tabla.column("Cliente", anchor=tk.W, width=150)
    tabla.column("Producto", anchor=tk.W, width=150)
    tabla.column("Cantidad", anchor=tk.CENTER, width=80)
    tabla.column("Total", anchor=tk.CENTER, width=100)
    tabla.column("Fecha", anchor=tk.CENTER, width=120)

    tabla.heading("#0", text="")
    tabla.heading("ID", text="ID")
    tabla.heading("Cliente", text="Cliente")
    tabla.heading("Producto", text="Producto")
    tabla.heading("Cantidad", text="Cantidad")
    tabla.heading("Total", text="Total")
    tabla.heading("Fecha", text="Fecha")

    tabla.pack(fill="both", expand=True, pady=10)

    # 🔹 CARGAR VENTAS
    def cargar_ventas():

        for fila in tabla.get_children():
            tabla.delete(fila)

        conexion = sqlite3.connect("EcoVerdeDB.db")
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT 
                ventas.id,
                clientes.nombre,
                productos.nombre,
                ventas.cantidad,
                ventas.total,
                ventas.fecha
            FROM ventas
            JOIN clientes ON ventas.cliente_id = clientes.id
            JOIN productos ON ventas.producto_id = productos.id
        """)

        ventas = cursor.fetchall()

        for venta in ventas:
            tabla.insert("", tk.END, values=venta)

        conexion.close()

    # 🔹 CARGAR DATOS AL INICIAR
    cargar_ventas()
