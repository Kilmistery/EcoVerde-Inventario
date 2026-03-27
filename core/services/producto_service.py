from config.database import get_connection


def listar_productos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, precio, stock FROM productos")
    data = cursor.fetchall()
    conn.close()
    return data


def crear_producto(nombre, precio, stock):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
        (nombre, precio, stock)
    )
    conn.commit()
    conn.close()


def actualizar_producto(id, nombre, precio, stock):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE productos SET nombre=?, precio=?, stock=? WHERE id=?",
        (nombre, precio, stock, id)
    )
    conn.commit()
    conn.close()


def eliminar_producto(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id=?", (id,))
    conn.commit()
    conn.close()