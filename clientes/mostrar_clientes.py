import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def ventana_clientes():

    ventana = tk.Toplevel()
    ventana.title("Clientes registrados")
    ventana.geometry("600x450")

    # TABLA
    tabla = ttk.Treeview(ventana)

    tabla["columns"] = ("ID", "Nombre", "Telefono")

    tabla.column("#0", width=0, stretch=tk.NO)
    tabla.column("ID", anchor=tk.CENTER, width=50)
    tabla.column("Nombre", anchor=tk.W, width=250)
    tabla.column("Telefono", anchor=tk.CENTER, width=150)

    tabla.heading("#0", text="")
    tabla.heading("ID", text="ID")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Telefono", text="Telefono")

    tabla.pack(fill="both", expand=True, pady=10)


    # FUNCION CARGAR CLIENTES
    def cargar_clientes():

        for fila in tabla.get_children():
            tabla.delete(fila)

        conexion = sqlite3.connect("EcoVerdeDB.db")
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM clientes")
        clientes = cursor.fetchall()

        for cliente in clientes:
            tabla.insert("", tk.END, values=cliente)

        conexion.close()


    # VENTANA NUEVO CLIENTE
    def nuevo_cliente():

        ventana_nuevo = tk.Toplevel()
        ventana_nuevo.grab_set()
        ventana_nuevo.title("Nuevo Cliente")
        ventana_nuevo.geometry("300x200")

        tk.Label(ventana_nuevo, text="Nombre").pack()
        entry_nombre = tk.Entry(ventana_nuevo)
        entry_nombre.pack()

        tk.Label(ventana_nuevo, text="Telefono").pack()
        entry_telefono = tk.Entry(ventana_nuevo)
        entry_telefono.pack()

        def guardar():

            nombre = entry_nombre.get()
            telefono = entry_telefono.get()
            
            if not nombre or not telefono:
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
                
            conexion = sqlite3.connect("EcoVerdeDB.db")
            cursor = conexion.cursor()

            cursor.execute(
                "INSERT INTO clientes (nombre, telefono) VALUES (?, ?)",
                (nombre, telefono)
            )

            conexion.commit()
            conexion.close()

            messagebox.showinfo("EcoVerde", "Cliente agregado")

            ventana_nuevo.destroy()
            cargar_clientes()

        tk.Button(ventana_nuevo, text="Guardar", command=guardar).pack(pady=10)


    # MODIFICAR CLIENTE
    def modificar_cliente():

        seleccionado = tabla.focus()

        if not seleccionado:
            messagebox.showwarning("EcoVerde", "Seleccione un cliente")
            return

        datos = tabla.item(seleccionado, "values")

        id_cliente = datos[0]

        ventana_modificar = tk.Toplevel()
        ventana_modificar.grab_set()
        ventana_modificar.title("Modificar Cliente")
        ventana_modificar.geometry("300x200")

        tk.Label(ventana_modificar, text="Nombre").pack()
        entry_nombre = tk.Entry(ventana_modificar)
        entry_nombre.insert(0, datos[1])
        entry_nombre.pack()

        tk.Label(ventana_modificar, text="Telefono").pack()
        entry_telefono = tk.Entry(ventana_modificar)
        entry_telefono.insert(0, datos[2])
        entry_telefono.pack()

        def guardar_cambios():

            nombre = entry_nombre.get()
            telefono = entry_telefono.get()

            conexion = sqlite3.connect("EcoVerdeDB.db")
            cursor = conexion.cursor()

            cursor.execute(
                "UPDATE clientes SET nombre=?, telefono=? WHERE id=?",
                (nombre, telefono, id_cliente)
            )

            conexion.commit()
            conexion.close()

            messagebox.showinfo("EcoVerde", "Cliente actualizado")

            ventana_modificar.destroy()
            cargar_clientes()

        tk.Button(ventana_modificar, text="Guardar cambios", command=guardar_cambios).pack(pady=10)


    # ELIMINAR CLIENTE
    def eliminar_cliente():

        seleccionado = tabla.focus()

        if not seleccionado:
            messagebox.showwarning("EcoVerde", "Seleccione un cliente")
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
                "DELETE FROM clientes WHERE id=?",
                (datos[0],)
            )

            conexion.commit()
            conexion.close()

            cargar_clientes()


    # BOTONES
    frame_botones = tk.Frame(ventana)
    frame_botones.pack(pady=10)

    tk.Button(
        frame_botones,
        text="Nuevo Cliente",
        width=15,
        command=nuevo_cliente
    ).grid(row=0, column=0, padx=5)

    tk.Button(
        frame_botones,
        text="Modificar",
        width=15,
        command=modificar_cliente
    ).grid(row=0, column=1, padx=5)

    tk.Button(
        frame_botones,
        text="Eliminar",
        width=15,
        command=eliminar_cliente
    ).grid(row=0, column=2, padx=5)


    # CARGAR DATOS
    cargar_clientes()