import tkinter as tk
from tkinter import ttk, messagebox
from core.services.cliente_service import *


def ventana_clientes():

    win = tk.Toplevel()
    win.title("Clientes")
    win.geometry("950x600")

    # 🔹 CONTENEDOR PRINCIPAL
    main = ttk.Frame(win)
    main.pack(fill="both", expand=True)

    # 🔹 SIDEBAR (SIN COLORES HARDCODEADOS)
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
        text="Gestión de Clientes",
        style="Title.TLabel"
    ).pack(side="left")

    # 🔹 BUSCADOR
    search_frame = ttk.Frame(header)
    search_frame.pack(side="right")

    ttk.Label(search_frame, text="Buscar cliente:").pack(side="left", padx=5)

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
        columns=("ID", "Nombre", "Telefono"),
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

    for col in ("ID", "Nombre", "Telefono"):
        tabla.heading(col, text=col, command=lambda c=col: ordenar(c, False))

    tabla.column("ID", width=60, anchor="center")
    tabla.column("Nombre", width=300)
    tabla.column("Telefono", width=150, anchor="center")

    tabla.pack(fill="both", expand=True)

    # 🔹 FILAS (SIN COLORES HARDCODEADOS)
    tabla.tag_configure("par", style="Treeview")
    tabla.tag_configure("impar", style="Treeview")

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
        datos = listar_clientes()

        for i, c in enumerate(datos):
            nombre = c[1].lower()
            telefono = str(c[2]).lower()

            if filtro in nombre or filtro in telefono:
                tag = "par" if i % 2 == 0 else "impar"
                tabla.insert("", tk.END, values=c, tags=(tag,))

    def buscar(*args):
        cargar(search_var.get())

    search_var.trace("w", buscar)

    # 🔹 NUEVO
    def nuevo():
        w = tk.Toplevel(win)
        w.title("Nuevo Cliente")
        w.geometry("350x250")

        frame = ttk.Frame(w, padding=15)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Nombre").pack(pady=5)
        e1 = ttk.Entry(frame)
        e1.pack(fill="x")

        ttk.Label(frame, text="Teléfono").pack(pady=5)
        e2 = ttk.Entry(frame)
        e2.pack(fill="x")

        def guardar():
            nombre = e1.get().strip()
            telefono = e2.get().strip()

            if not nombre:
                messagebox.showwarning("Error", "Nombre obligatorio")
                return

            crear_cliente(nombre, telefono)
            w.destroy()
            cargar()

        ttk.Button(frame, text="Guardar").pack(pady=15)

    # 🔹 EDITAR
    def editar(event=None):
        selected = tabla.focus()
        if not selected:
            return

        datos = tabla.item(selected, "values")

        w = tk.Toplevel(win)
        w.title("Editar Cliente")
        w.geometry("350x250")

        frame = ttk.Frame(w, padding=15)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Nombre").pack(pady=5)
        e1 = ttk.Entry(frame)
        e1.insert(0, datos[1])
        e1.pack(fill="x")

        ttk.Label(frame, text="Teléfono").pack(pady=5)
        e2 = ttk.Entry(frame)
        e2.insert(0, datos[2])
        e2.pack(fill="x")

        def guardar():
            actualizar_cliente(datos[0], e1.get(), e2.get())
            w.destroy()
            cargar()

        ttk.Button(frame, text="Guardar cambios", command=guardar).pack(pady=15)

    tabla.bind("<Double-1>", editar)

    # 🔹 ELIMINAR
    def eliminar():
        selected = tabla.focus()

        if not selected:
            messagebox.showwarning("Atención", "Selecciona un cliente")
            return

        datos = tabla.item(selected, "values")

        confirm = messagebox.askyesno("Confirmar", f"¿Eliminar a {datos[1]}?")

        if confirm:
            eliminar_cliente(datos[0])
            cargar()

    # 🔹 BOTONES
    acciones = ttk.Frame(content)
    acciones.pack(fill="x", pady=10)

    ttk.Button(acciones, text="➕ Nuevo", command=nuevo).pack(side="left", padx=5)
    ttk.Button(acciones, text="🗑 Eliminar", command=eliminar).pack(side="left", padx=5)

    # 🔹 CARGA
    cargar()