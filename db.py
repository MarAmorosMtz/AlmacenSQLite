import sqlite3

# Conexión con la base de datos
conn = sqlite3.connect('store.db')
c = conn.cursor()

# Crear la tabla de productos si no existe
c.execute("""
CREATE TABLE productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    descripcion TEXT,
    marca TEXT,
    tamaño TEXT,
    tipo_entrada TEXT
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
c.execute("""INSERT OR IGNORE INTO usuarios VALUES('admin', 'admin', 'su')""")
conn.commit()

# Función para agregar un producto a la base de datos
def agregar_producto(id, nombre, descripcion, marca, tamaño, tipo_entrada):
    if id and nombre and marca and tamaño and tipo_entrada:
        c.execute("INSERT INTO productos VALUES (?, ?, ?, ?, ?, ?)", (id, nombre, descripcion, marca, tamaño, tipo_entrada))
        conn.commit()
        print("Producto agregado correctamente")
    else:
        print("Todos los campos son obligatorios")

# Función para actualizar un producto en la base de datos
def editar_producto(id, nombre, descripcion, marca, tamaño, tipo_entrada):
    if id and nombre and marca and tamaño and tipo_entrada:
        c.execute("""UPDATE productos SET nombre=?, descripcion=?, marca=?, tamaño=?, tipo_entrada=? WHERE id=?""",
                  (nombre, descripcion, marca, tamaño, tipo_entrada, id))
        conn.commit()
        print("Producto actualizado correctamente")
    else:
        print("Todos los campos son obligatorios")

# Función para eliminar un producto de la base de datos
def eliminar_producto(id):
    c.execute("DELETE FROM productos WHERE id=?", (id,))
    conn.commit()
    print("Producto eliminado correctamente")

# Función para obtener todos los productos
def obtener_productos():
    c.execute("SELECT * FROM productos")
    productos = c.fetchall()
    return productos

# Función para obtener un producto específico por su ID
def obtener_producto_por_id(id):
    c.execute("SELECT * FROM productos WHERE id=?", (id,))
    producto = c.fetchone()
    return producto

# Cerrar la conexión con la base de datos (llamar al final del programa)
def cerrar_conexion():
    conn.close()

# Ejemplo de uso
# Agregar un producto
# agregar_producto('1', 'Producto 1', 'Descripción del producto 1', 'Marca A', 'Pequeño', 'Entrada Manual')

# Cerrar la conexión
cerrar_conexion()
