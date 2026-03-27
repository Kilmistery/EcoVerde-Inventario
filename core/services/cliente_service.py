import sqlite3

DB = "data/EcoVerdeDB.db"

def conectar():
    return sqlite3.connect(DB)

def listar_clientes():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM clientes")
    datos = cur.fetchall()
    con.close()
    return datos

def crear_cliente(nombre, telefono):
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO clientes (nombre, telefono) VALUES (?, ?)",
        (nombre, telefono)
    )
    con.commit()
    con.close()

def actualizar_cliente(id, nombre, telefono):
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "UPDATE clientes SET nombre=?, telefono=? WHERE id=?",
        (nombre, telefono, id)
    )
    con.commit()
    con.close()

def eliminar_cliente(id):
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM clientes WHERE id=?", (id,))
    con.commit()
    con.close()