import tkinter as tk
from tkinter import ttk, messagebox
from core.services.producto_service import *


def ventana_productos():

    win = tk.Toplevel()
    win.title("Productos")
    win.geometry("950x600")

    # 🔹 CONTENEDOR PRINCIPAL
    main = ttk.Frame(win)
    main.pack(fill="both", expand=True)

    # 🔹 SIDEBAR
    sidebar = ttk.Frame(main, style="Sidebar.TFrame", width=180)
    sidebar.pack(side="left", fill="y")

    ttk.Label(
        sidebar,
        text="EcoVerde",
        style="SidebarTitle.TLabel"
    ).pack(pady=20)

    # 🔹 CONTENIDO
    content = ttk.Frame(main, padding=15)
    content.pack(side="right", fill="both", expand=True)

    # 🔹 HEADER
    header = ttk.Frame(content)
    header.pack(fill="x")

    ttk.Label(
        header,
        text="Gestión de Productos",
        style="Title.TLabel"
    ).pack(side="left")

    # 🔹 BUSCADOR
    search_frame = ttk.Frame(header)
    search_frame.pack(side="right")

    ttk.Label(search_frame, text="Buscar producto:").pack(side="left", padx=5)

    search_var = tk.StringVar()

    search = ttk.Entry(search_frame, textvariable=search_var, width=30)
    search.pack(side="left")

    def limpiar_busqueda():
        search_var.set("")
        cargar()

    ttk.Button(search_frame, text="✖", width=3, command=limpiar_busqueda).pack(side="left", padx=5)

    # 🔹 TABLA
    frame_tabla = ttk.Frame(content)
    frame_tabla.pack(fill="both", expand=True, pady=10)

    scroll = ttk.Scrollbar(frame_tabla)
    scroll.pack(side="right", fill="y")

    tabla = ttk.Treeview(
        frame_tabla,
        columns=("ID", "Nombre", "Precio", "Stock"),
        show="headings",
        yscrollcommand=scroll.set
    )

    scroll.config(command=tabla.yview)

    # 🔹 ORDENAR COLUMNAS
    def ordenar(col, reverse):
        datos = [(tabla.set(k, col), k) for k in tabla.get_children("")]
        datos.sort(reverse=reverse)

        for index, (val, k) in enumerate(datos):
            tabla.move(k, "", index)

        tabla.heading(col, command=lambda: ordenar(col, not reverse))

    for col in ("ID", "Nombre", "Precio", "Stock"):
        tabla.heading(col, text=col, command=lambda c=col: ordenar(c, False))

    tabla.column("ID", width=60, anchor="center")
    tabla.column("Nombre", width=300)
    tabla.column("Precio", width=120, anchor="center")
    tabla.column("Stock", width=120, anchor="center")

    tabla.pack(fill="both", expand=True)

    # 🔹 FILAS (CORREGIDO ❗)
    tabla.tag_configure("par", background="#f2f2f2")
    tabla.tag_configure("impar", background="white")

    # 🔹 HOVER
    def on_hover(event):
        item = tabla.identify_row(event.y)
        if item:
            tabla.selection_set(item)

    tabla.bind("<Motion>", on_hover)

    # 🔹 FUNCIONES
    def cargar(filtro=""):
        tabla.delete(*tabla.get_children())

        filtro = filtro.strip().lower()
        datos = listar_productos()

        for i, p in enumerate(datos):
            nombre = str(p[1]).lower()

            if filtro in nombre:
                tag = "par" if i % 2 == 0 else "impar"
                tabla.insert("", tk.END, values=p, tags=(tag,))

    def buscar(*args):
        cargar(search_var.get())

    search_var.trace("w", buscar)

    # 🔹 NUEVO
    def nuevo():
        w = tk.Toplevel(win)
        w.title("Nuevo Producto")
        w.geometry("350x300")

        frame = ttk.Frame(w, padding=15)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Nombre").pack(pady=5)
        e1 = ttk.Entry(frame)
        e1.pack(fill="x")

        ttk.Label(frame, text="Precio").pack(pady=5)
        e2 = ttk.Entry(frame)
        e2.pack(fill="x")

        ttk.Label(frame, text="Stock").pack(pady=5)
        e3 = ttk.Entry(frame)
        e3.pack(fill="x")

        def guardar():
            nombre = e1.get().strip()
            precio = e2.get().strip()
            stock = e3.get().strip()

            if not nombre:
                messagebox.showwarning("Error", "Nombre obligatorio")
                return

            crear_producto(nombre, precio, stock)
            w.destroy()
            cargar()

        ttk.Button(frame, text="Guardar", command=guardar).pack(pady=15)

    # 🔹 EDITAR
    def editar(event=None):
        selected = tabla.focus()
        if not selected:
            return

        datos = tabla.item(selected, "values")

        w = tk.Toplevel(win)
        w.title("Editar Producto")
        w.geometry("350x300")

        frame = ttk.Frame(w, padding=15)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Nombre").pack(pady=5)
        e1 = ttk.Entry(frame)
        e1.insert(0, datos[1])
        e1.pack(fill="x")

        ttk.Label(frame, text="Precio").pack(pady=5)
        e2 = ttk.Entry(frame)
        e2.insert(0, datos[2])
        e2.pack(fill="x")

        ttk.Label(frame, text="Stock").pack(pady=5)
        e3 = ttk.Entry(frame)
        e3.insert(0, datos[3])
        e3.pack(fill="x")

        def guardar():
            actualizar_producto(datos[0], e1.get(), e2.get(), e3.get())
            w.destroy()
            cargar()

        ttk.Button(frame, text="Guardar cambios", command=guardar).pack(pady=15)

    tabla.bind("<Double-1>", editar)

    # 🔹 ELIMINAR
    def eliminar():
        selected = tabla.focus()

        if not selected:
            messagebox.showwarning("Atención", "Selecciona un producto")
            return

        datos = tabla.item(selected, "values")

        confirm = messagebox.askyesno("Confirmar", f"¿Eliminar {datos[1]}?")

        if confirm:
            eliminar_producto(datos[0])
            cargar()

    # 🔹 BOTONES
    acciones = ttk.Frame(content)
    acciones.pack(fill="x", pady=10)

    ttk.Button(acciones, text="➕ Nuevo", command=nuevo).pack(side="left", padx=5)
    ttk.Button(acciones, text="🗑 Eliminar", command=eliminar).pack(side="left", padx=5)

    # 🔹 CARGA
    cargar()