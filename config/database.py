import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "EcoVerdeDB.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        telefono TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        precio REAL,
        stock REAL
    )
    """)

    conn.commit()
    conn.close()



def obtener_productos():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT id, nombre, precio, stock FROM productos")
    productos = cursor.fetchall()

    conn.close()
    return [dict(p) for p in productos]


def insertar_producto(nombre, precio, stock):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
        (nombre, precio, stock)
    )

    conn.commit()
    conn.close()


def eliminar_producto(id_producto):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))

    conn.commit()
    conn.close()