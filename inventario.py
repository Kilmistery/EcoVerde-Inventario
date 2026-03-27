import tkinter as tk
from tkinter import ttk

from config.database import init_db
from ui.styles.style import configurar_estilos

from ui.views.clientes.clientes_view import ventana_clientes
from ui.views.productos.productos_view import ventana_productos


def main():
    # 🔹 Inicializar DB
    init_db()

    # 🔹 Crear ventana principal
    root = tk.Tk()
    root.title("Sistema EcoVerde")
    root.geometry("500x450")

    # 🔹 Aplicar estilos
    configurar_estilos()

    # 🔹 CONTENEDOR PRINCIPAL
    container = ttk.Frame(root, padding=20)
    container.pack(fill="both", expand=True)

    # 🔹 TÍTULO
    titulo = ttk.Label(
        container,
        text="Sistema EcoVerde",
        font=("Segoe UI", 18, "bold")
    )
    titulo.pack(pady=20)

    # 🔹 SUBTÍTULO
    subtitulo = ttk.Label(
        container,
        text="Panel principal",
        font=("Segoe UI", 10)
    )
    subtitulo.pack(pady=5)

    # 🔹 SEPARADOR
    ttk.Separator(container).pack(fill="x", pady=15)

    # 🔹 BOTONES
    ttk.Button(
        container,
        text="Clientes",
        command=ventana_clientes
    ).pack(fill="x", pady=5)

    ttk.Button(
        container,
        text="Productos",
        command=ventana_productos
    ).pack(fill="x", pady=5)

    ttk.Button(
        container,
        text="Ventas (próximamente)",
        state="disabled"
    ).pack(fill="x", pady=5)

    ttk.Button(
        container,
        text="Consignación (próximamente)",
        state="disabled"
    ).pack(fill="x", pady=5)

    # 🔹 FOOTER
    ttk.Label(
        container,
        text="EcoVerde © 2026",
        font=("Segoe UI", 8)
    ).pack(side="bottom", pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()