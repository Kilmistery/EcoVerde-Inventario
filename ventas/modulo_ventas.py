import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def ventana_ventas():

    ventana = tk.Toplevel()
    ventana.title("Ventas")
    ventana.geometry("400x400")

    # CLIENTES
    tk.Label(ventana, text="Cliente").pack()
    combo_clientes = ttk.Combobox(ventana)
    combo_clientes.pack()

    # PRODUCTOS
    tk.Label(ventana, text="Producto").pack()
    combo_productos = ttk.Combobox(ventana)
    combo_productos.pack()

    # CANTIDAD
    tk.Label(ventana, text="Cantidad").pack()
    entry_cantidad = tk.Entry(ventana)
    entry_cantidad.pack()

    # 🔹 CARGAR DATOS
    def cargar_datos():

        conexion = sqlite3.connect("EcoVerdeDB.db")
        cursor = conexion.cursor()

        cursor.execute("SELECT id, nombre FROM clientes")
        clientes = cursor.fetchall()
        combo_clientes["values"] = [f"{c[0]} - {c[1]}" for c in clientes]

        cursor.execute("SELECT id, nombre FROM productos")
        productos = cursor.fetchall()
        combo_productos["values"] = [f"{p[0]} - {p[1]}" for p in productos]

        conexion.close()

    # 🔹 GUARDAR VENTA
    def guardar_venta():

        cliente = combo_clientes.get()
        producto = combo_productos.get()
        cantidad = entry_cantidad.get()

        # VALIDACIONES
        if not cliente or not producto or not cantidad:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            cantidad = int(cantidad)
        except:
            messagebox.showerror("Error", "Cantidad inválida")
            return

        cliente_id = cliente.split(" - ")[0]
        producto_id = producto.split(" - ")[0]

        conexion = sqlite3.connect("EcoVerdeDB.db")
        cursor = conexion.cursor()

        cursor.execute("SELECT precio FROM productos WHERE id=?", (producto_id,))
        resultado = cursor.fetchone()

        if not resultado:
            messagebox.showerror("Error", "Producto no encontrado")
            conexion.close()
            return

        precio = resultado[0]
        total = precio * cantidad

        cursor.execute(
            "INSERT INTO ventas (cliente_id, producto_id, cantidad, total, fecha) VALUES (?, ?, ?, ?, DATE('now'))",
            (cliente_id, producto_id, cantidad, total)
        )

        conexion.commit()
        conexion.close()

        messagebox.showinfo("EcoVerde", f"Venta registrada. Total: {total}")

        # limpiar campo
        entry_cantidad.delete(0, tk.END)

    # 🔹 BOTÓN
    tk.Button(ventana, text="Guardar venta", command=guardar_venta).pack(pady=15)

    # 🔹 CARGAR DATOS AL INICIAR
    cargar_datos()