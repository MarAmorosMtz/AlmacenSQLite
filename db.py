import sqlite3

# Conexión con la base de datos
conn = sqlite3.connect('store.db')
c = conn.cursor()

# Crear la tabla de consumibles si no existe
c.execute("""
CREATE TABLE IF NOT EXISTS consumibles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    descripcion TEXT,
    marca TEXT,
    tamaño TEXT,
    umed TEXT,
    cantidad INTEGER,
    nota TEXT
);
""")

# Crear la tabla de equipos si no existe
c.execute("""
CREATE TABLE IF NOT EXISTS equipos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag TEXT,
    nombre TEXT,
    descripcion TEXT,
    marca TEXT,
    tamaño TEXT,
    umed TEXT,
    cantidad INTEGER,
    nota TEXT
);
""")


# Crear la tabla de usuarios si no existe
c.execute("""
CREATE TABLE IF NOT EXISTS usuarios(
    nombre TEXT,
    pass TEXT,
    rol TEXT
);
""")

# Insertar el usuario admin si no existe
c.execute("""INSERT OR IGNORE INTO usuarios VALUES('admin', 'admin', 'admin')""")
conn.commit()

# Función para agregar un consumible a la base de datos
def agregar_consumible(id, nombre, descripcion, marca, tamaño, umed, cantidad, nota):
    if id and nombre and marca and tamaño and umed:
        c.execute("INSERT INTO consumibles VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (id, nombre, descripcion, marca, tamaño, umed, cantidad, nota))
        conn.commit()
        print("Consumible agregado correctamente")
    else:
        print("Todos los campos son obligatorios")

# Función para actualizar un consumible en la base de datos
def editar_consumible(id, nombre, descripcion, marca, tamaño, umed, cantidad, nota):
    if id and nombre and marca and tamaño and umed:
        c.execute("""UPDATE consumibles SET nombre=?, descripcion=?, marca=?, tamaño=?, umed=?, cantidad=?, nota=? WHERE id=?""",
                  (nombre, descripcion, marca, tamaño, umed, cantidad, nota, id))
        conn.commit()
        print("Consumible actualizado correctamente")
    else:
        print("Todos los campos son obligatorios")

# Función para eliminar un consumible de la base de datos
def eliminar_consumible(id):
    c.execute("DELETE FROM consumibles WHERE id=?", (id,))
    conn.commit()
    print("Consumible eliminado correctamente")

# Función para obtener todos los consumibles
def obtener_consumibles():
    c.execute("SELECT * FROM consumibles")
    consumibles = c.fetchall()
    return consumibles

# Función para obtener un consumible específico por su ID
def obtener_consumible_por_id(id):
    c.execute("SELECT * FROM consumibles WHERE id=?", (id,))
    consumible = c.fetchone()
    return consumible


# Función para agregar un equipo a la base de datos
def agregar_equipo(id, tag, nombre, descripcion, marca, tamaño, umed, cantidad, nota):
    if id and tag and nombre and marca and tamaño and umed:
        c.execute("INSERT INTO equipos VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (id, tag, nombre, descripcion, marca, tamaño, umed, cantidad, nota))
        conn.commit()
        print("Equipo agregado correctamente")
    else:
        print("Todos los campos son obligatorios")

# Función para actualizar un equipo en la base de datos
def editar_equipo(id, tag, nombre, descripcion, marca, tamaño, umed, cantidad, nota):
    if id and tag and nombre and marca and tamaño and umed:
        c.execute("""UPDATE equipos SET tag=?, nombre=?, descripcion=?, marca=?, tamaño=?, umed=?, cantidad=?, nota=? WHERE id=?""",
                  (tag, nombre, descripcion, marca, tamaño, umed, cantidad, nota, id))
        conn.commit()
        print("Equipo actualizado correctamente")
    else:
        print("Todos los campos son obligatorios")

# Función para eliminar un equipo de la base de datos
def eliminar_equipo(id):
    c.execute("DELETE FROM equipos WHERE id=?", (id,))
    conn.commit()
    print("Equipo eliminado correctamente")

# Función para obtener todos los equipos
def obtener_equipos():
    c.execute("SELECT * FROM equipos")
    equipos = c.fetchall()
    return equipos

# Función para obtener un equipo específico por su ID
def obtener_equipo_por_id(id):
    c.execute("SELECT * FROM equipos WHERE id=?", (id,))
    equipo = c.fetchone()
    return equipo


# Cerrar la conexión con la base de datos (llamar al final del programa)
def cerrar_conexion():
    conn.close()

# Cerrar la conexión
cerrar_conexion()
