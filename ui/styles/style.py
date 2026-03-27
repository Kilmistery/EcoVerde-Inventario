from tkinter import ttk

def configurar_estilos():
    style = ttk.Style()
    style.theme_use("clam")

    # 🎨 PALETA ECO
    bg = "#F4F8F5"          # fondo claro verdoso
    primary = "#2E7D32"     # verde principal (botones)
    hover = "#1B5E20"       # verde oscuro hover
    accent = "#A5D6A7"      # verde suave
    text = "#1B4332"        # texto oscuro natural
    white = "#FFFFFF"
    border = "#DDE5DC"

    # 🔹 GENERAL
    style.configure("TFrame", background=bg)
    style.configure(
        "TLabel",
        background=bg,
        foreground=text,
        font=("Segoe UI", 10)
    )

    # 🔹 BOTONES
    style.configure(
        "TButton",
        background=primary,
        foreground="white",
        font=("Segoe UI", 10, "bold"),
        padding=8,
        borderwidth=0
    )

    style.map(
        "TButton",
        background=[("active", hover)],
        foreground=[("active", "white")]
    )

    # 🔹 INPUTS
    style.configure(
        "TEntry",
        padding=6,
        fieldbackground="white"
    )

    # 🔹 TABLA
    style.configure(
        "Treeview",
        background=white,
        foreground=text,
        rowheight=30,
        fieldbackground=white,
        bordercolor=border
    )

    style.configure(
        "Treeview.Heading",
        background=accent,
        foreground=text,
        font=("Segoe UI", 10, "bold")
    )

    style.map(
        "Treeview",
        background=[("selected", primary)],
        foreground=[("selected", "white")]
    )