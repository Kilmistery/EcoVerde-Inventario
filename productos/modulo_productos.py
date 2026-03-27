import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def ventana_productos():

    ventana = tk.Toplevel()
    ventana.title("Productos registrados")
    ventana.geometry("800x650")

    # TABLA
    tabla = ttk.Treeview(ventana)

    tabla["columns"] = ("ID", "Nombre", "Precio", "Stock")

    tabla.column("#0", width=0, stretch=tk.NO)
    tabla.column("ID", anchor=tk.CENTER, width=50)
    tabla.column("Nombre", anchor=tk.W, width=250)
    tabla.column("Precio", anchor=tk.CENTER, width=150)
    tabla.column("Stock", anchor=tk.CENTER, width=350)


    tabla.heading("#0", text="")
    tabla.heading("ID", text="ID")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Precio", text="Precio")
    tabla.heading("Stock", text="Stock")

    tabla.pack(fill="both", expand=True, pady=10)


    # FUNCION CARGAR CLIENTES
    def cargar_productos():

        for fila in tabla.get_children():
            tabla.delete(fila)

        conexion = sqlite3.connect("EcoVerdeDB.db")
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()

        for productos in productos:
            tabla.insert("", tk.END, values=productos)

        conexion.close()


    # VENTANA NUEVO CLIENTE
    def nuevo_producto():

        ventana_nuevo = tk.Toplevel()
        ventana_nuevo.title("Nuevo Producto")
        ventana_nuevo.geometry("300x200")

        tk.Label(ventana_nuevo, text="Nombre").pack()
        entry_nombre = tk.Entry(ventana_nuevo)
        entry_nombre.pack()

        tk.Label(ventana_nuevo, text="Precio").pack()
        entry_Precio = tk.Entry(ventana_nuevo)
        entry_Precio.pack()

        tk.Label(ventana_nuevo, text="Stock").pack()
        entry_Stock = tk.Entry(ventana_nuevo)
        entry_Stock.pack()

        def guardar():

            nombre = entry_nombre.get()
            precio = entry_Precio.get()
            stock = entry_Stock.get()

            conexion = sqlite3.connect("EcoVerdeDB.db")
            cursor = conexion.cursor()

            cursor.execute(
                "INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
                (nombre, precio, stock)
            )

            conexion.commit()
            conexion.close()

            messagebox.showinfo("EcoVerde", "Producto agregado")

            ventana_nuevo.destroy()
            cargar_productos()

        tk.Button(ventana_nuevo, text="Guardar", command=guardar).pack(pady=10)


    # MODIFICAR CLIENTE
    def modificar_producto():

        seleccionado = tabla.focus()

        if not seleccionado:
            messagebox.showwarning("EcoVerde", "Seleccione un producto")
            return

        datos = tabla.item(seleccionado, "values")

        id_producto = datos[0]

        ventana_modificar = tk.Toplevel()
        ventana_modificar.title("Modificar Producto")
        ventana_modificar.geometry("300x200")

        tk.Label(ventana_modificar, text="Nombre").pack()
        entry_nombre = tk.Entry(ventana_modificar)
        entry_nombre.insert(0, datos[1])
        entry_nombre.pack()

        tk.Label(ventana_modificar, text="Precio").pack()
        entry_precio = tk.Entry(ventana_modificar)
        entry_precio.insert(0, datos[2])
        entry_precio.pack()

        tk.Label(ventana_modificar, text="Stock").pack()
        entry_stock = tk.Entry(ventana_modificar)
        entry_stock.insert(0, datos[3])
        entry_stock.pack()

        def guardar_cambios():

            nombre = entry_nombre.get()
            precio = entry_precio.get()
            stock = entry_stock.get()

            conexion = sqlite3.connect("EcoVerdeDB.db")
            cursor = conexion.cursor()

            cursor.execute(
                "UPDATE productos SET nombre=?, precio=?, stock=? WHERE id=?",
                (nombre, precio, stock)
            )

            conexion.commit()
            conexion.close()

            messagebox.showinfo("EcoVerde", "Producto actualizado")

            ventana_modificar.destroy()
            cargar_productos()

        tk.Button(ventana_modificar, text="Guardar cambios", command=guardar_cambios).pack(pady=10)


    # ELIMINAR CLIENTE
    def eliminar_producto():

        seleccionado = tabla.focus()

        if not seleccionado:
            messagebox.showwarning("EcoVerde", "Seleccione un producto")
            return

        datos = tabla.item(seleccionado, "values")

        confirmar = messagebox.askyesno(
            "EcoVerde",
            "¿Eliminar cliente seleccionado?"
        )

        if confirmar:

            conexion = sqlite3.connect("EcoVerdeDB.db")
            cursor = conexion.cursor()

            cursor.execute(
                "DELETE FROM productos WHERE id=?",
                (datos[0],)
            )

            conexion.commit()
            conexion.close()

            cargar_productos()


    # BOTONES
    frame_botones = tk.Frame(ventana)
    frame_botones.pack(pady=10)

    tk.Button(
        frame_botones,
        text="Nuevo producto",
        width=15,
        command=nuevo_producto
    ).grid(row=0, column=0, padx=5)

    tk.Button(
        frame_botones,
        text="Modificar",
        width=15,
        command=modificar_producto
    ).grid(row=0, column=1, padx=5)

    tk.Button(
        frame_botones,
        text="Eliminar",
        width=15,
        command=eliminar_producto
    ).grid(row=0, column=2, padx=5)


    # CARGAR DATOS
    cargar_productos()