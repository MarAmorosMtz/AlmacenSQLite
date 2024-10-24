import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Conexión con la base de datos
conn = sqlite3.connect('store.db')
c = conn.cursor()

# Función para verificar el login desde la base de datos
def verificar_login():
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()

    # Verificar credenciales en la base de datos
    c.execute("SELECT * FROM usuarios WHERE nombre=? AND pass=?", (usuario, contraseña))
    result = c.fetchone()

    if result:
        ventana.destroy()  # Cierra la ventana de login
        abrir_nueva_ventana()  # Abre la nueva ventana
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

# Función para mostrar el menú de opciones (editar/eliminar)
def mostrar_menu(event, item_id):
    menu = tk.Menu(tabla, tearoff=0)
    menu.add_command(label="Editar", command=lambda: editar_entrada(item_id))
    menu.add_command(label="Eliminar", command=lambda: eliminar_entrada(item_id))
    menu.post(event.x_root, event.y_root)

# Función para editar la entrada
def editar_entrada(item_id):
    entrada = tabla.item(item_id)['values']
    abrir_ventana_editar(entrada)

# Función para abrir la ventana de edición
def abrir_ventana_editar(entrada):
    def actualizar_producto():
        nuevo_nombre = entry_nombre.get()
        nueva_descripcion = entry_descripcion.get()
        nueva_marca = entry_marca.get()
        nuevo_tamaño = entry_tamaño.get()
        nuevo_tipo_entrada = entry_tipo_entrada.get()

        if nuevo_nombre and nueva_descripcion and nueva_marca and nuevo_tamaño and nuevo_tipo_entrada:
            c.execute("UPDATE productos SET nombre=?, descripcion=?, marca=?, tamaño=?, tipo_entrada=? WHERE id=?",
                      (nuevo_nombre, nueva_descripcion, nueva_marca, nuevo_tamaño, nuevo_tipo_entrada, entrada[0]))
            conn.commit()
            messagebox.showinfo("Actualizar Producto", "Producto actualizado correctamente.")
            actualizar_tabla()
            editar_ventana.destroy()  # Cerrar ventana de edición
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")

    editar_ventana = tk.Toplevel()
    editar_ventana.title("Editar Producto")
    editar_ventana.geometry("400x400")

    tk.Label(editar_ventana, text="Nombre:", font=('Arial', 12)).pack(pady=5)
    entry_nombre = tk.Entry(editar_ventana, font=('Arial', 12))
    entry_nombre.pack(pady=5)
    entry_nombre.insert(0, entrada[1])  # Rellenar con el nombre actual

    tk.Label(editar_ventana, text="Descripción:", font=('Arial', 12)).pack(pady=5)
    entry_descripcion = tk.Entry(editar_ventana, font=('Arial', 12))
    entry_descripcion.pack(pady=5)
    entry_descripcion.insert(0, entrada[2])  # Rellenar con la descripción actual

    tk.Label(editar_ventana, text="Marca:", font=('Arial', 12)).pack(pady=5)
    entry_marca = tk.Entry(editar_ventana, font=('Arial', 12))
    entry_marca.pack(pady=5)
    entry_marca.insert(0, entrada[3])  # Rellenar con la marca actual

    tk.Label(editar_ventana, text="Tamaño:", font=('Arial', 12)).pack(pady=5)
    entry_tamaño = tk.Entry(editar_ventana, font=('Arial', 12))
    entry_tamaño.pack(pady=5)
    entry_tamaño.insert(0, entrada[4])  # Rellenar con el tamaño actual

    tk.Label(editar_ventana, text="Tipo de Entrada:", font=('Arial', 12)).pack(pady=5)
    entry_tipo_entrada = tk.Entry(editar_ventana, font=('Arial', 12))
    entry_tipo_entrada.pack(pady=5)
    entry_tipo_entrada.insert(0, entrada[5])  # Rellenar con el tipo de entrada actual

    # Botón de actualizar
    boton_actualizar = tk.Button(editar_ventana, text="Actualizar", font=('Arial', 12), command=actualizar_producto)
    boton_actualizar.pack(pady=20)

    # Botón de cancelar
    boton_cancelar = tk.Button(editar_ventana, text="Cancelar", font=('Arial', 12), command=editar_ventana.destroy)
    boton_cancelar.pack(pady=5)

# Función para eliminar la entrada
def eliminar_entrada(item_id):
    entrada = tabla.item(item_id)['values']
    confirmar = messagebox.askyesno("Eliminar", f"¿Seguro que deseas eliminar el producto {entrada[1]}?")
    if confirmar:
        # Eliminar de la base de datos
        c.execute("DELETE FROM productos WHERE id=?", (entrada[0],))
        conn.commit()
        actualizar_tabla()

# Función para abrir la nueva ventana con la tabla
def abrir_nueva_ventana():
    global tabla
    global entry_nombre, entry_marca, entry_tamaño, entry_descripcion, entry_tipo_entrada  # Hacer accesibles los campos del formulario

    nueva_ventana = tk.Tk()
    nueva_ventana.title("Dashboard")
    nueva_ventana.geometry("800x600")

    # Crear contenedor de pestañas
    tab_control = ttk.Notebook(nueva_ventana)
    tab_principal = ttk.Frame(tab_control)
    tab_opciones = ttk.Frame(tab_control)

    tab_control.add(tab_principal, text="Principal")
    tab_control.add(tab_opciones, text="Agregar")
    tab_control.pack(expand=1, fill='both')

    # ----- Pestaña Principal -----
    # Crear cuadro de búsqueda
    lbl_buscar = tk.Label(tab_principal, text="Buscar:", font=('Arial', 14))
    lbl_buscar.pack(pady=10)
    entry_buscar = tk.Entry(tab_principal, width=50, font=('Arial', 14))
    entry_buscar.pack(pady=10)

    # Crear tabla
    columnas = ("ID", "Nombre", "Descripción", "Marca", "Tamaño", "Tipo de Entrada", "Opciones")
    tabla = ttk.Treeview(tab_principal, columns=columnas, show="headings")
    tabla.heading("ID", text="ID")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Descripción", text="Descripción")
    tabla.heading("Marca", text="Marca")
    tabla.heading("Tamaño", text="Tamaño")
    tabla.heading("Tipo de Entrada", text="Tipo de Entrada")
    tabla.heading("Opciones", text="Opciones")

    # Definir el ancho de las columnas
    tabla.column("ID", width=50)
    tabla.column("Nombre", width=150)
    tabla.column("Descripción", width=150)
    tabla.column("Marca", width=100)
    tabla.column("Tamaño", width=100)
    tabla.column("Tipo de Entrada", width=100)
    tabla.column("Opciones", width=100)

    tabla.pack(pady=20, expand=True, fill='both')

    # Evento para detectar clic en la columna "Opciones"
    def on_click(event):
        # Obtener la posición del clic y el elemento seleccionado
        item_id = tabla.identify_row(event.y)
        column = tabla.identify_column(event.x)

        # Verificar si se hizo clic en la columna "Opciones"
        if column == '#7' and item_id:
            mostrar_menu(event, item_id)

    # Vincular el evento clic a la tabla
    tabla.bind("<Button-1>", on_click)

    # Cargar datos de la base de datos en la tabla
    actualizar_tabla()

    # ----- Pestaña de Opciones -----
    lbl_opciones = tk.Label(tab_opciones, text="Agregar Nuevos Productos", font=('Arial', 16))
    lbl_opciones.pack(pady=20)

    # Formulario para agregar nuevo producto
    tk.Label(tab_opciones, text="Nombre:", font=('Arial', 14)).pack(pady=5)
    entry_nombre = tk.Entry(tab_opciones, font=('Arial', 14))
    entry_nombre.pack(pady=5)

    tk.Label(tab_opciones, text="Descripción:", font=('Arial', 14)).pack(pady=5)
    entry_descripcion = tk.Entry(tab_opciones, font=('Arial', 14))
    entry_descripcion.pack(pady=5)

    tk.Label(tab_opciones, text="Marca:", font=('Arial', 14)).pack(pady=5)
    entry_marca = tk.Entry(tab_opciones, font=('Arial', 14))
    entry_marca.pack(pady=5)

    tk.Label(tab_opciones, text="Tamaño:", font=('Arial', 14)).pack(pady=5)
    entry_tamaño = tk.Entry(tab_opciones, font=('Arial', 14))
    entry_tamaño.pack(pady=5)

    tk.Label(tab_opciones, text="Tipo de Entrada:", font=('Arial', 14)).pack(pady=5)
    entry_tipo_entrada = tk.Entry(tab_opciones, font=('Arial', 14))
    entry_tipo_entrada.pack(pady=5)

    # Botón para agregar el producto
    boton_agregar = tk.Button(tab_opciones, text="Agregar Producto", font=('Arial', 14), command=agregar_producto)
    boton_agregar.pack(pady=20)

    nueva_ventana.mainloop()

# Función para agregar un producto a la base de datos
def agregar_producto():
    nombre = entry_nombre.get()
    descripcion = entry_descripcion.get()
    marca = entry_marca.get()
    tamaño = entry_tamaño.get()
    tipo_entrada = entry_tipo_entrada.get()

    if nombre and descripcion and marca and tamaño and tipo_entrada:
        # Obtener el próximo ID automático
        c.execute("SELECT COUNT(*) FROM productos")
        nuevo_id = c.fetchone()[0] + 1  # Genera un nuevo ID
        c.execute("INSERT INTO productos (id, nombre, descripcion, marca, tamaño, tipo_entrada) VALUES (?, ?, ?, ?, ?, ?)",
                  (nuevo_id, nombre, descripcion, marca, tamaño, tipo_entrada))
        conn.commit()
        messagebox.showinfo("Agregar Producto", "Producto agregado correctamente.")
        actualizar_tabla()
        entry_nombre.delete(0, tk.END)  # Limpiar el campo de entrada
        entry_descripcion.delete(0, tk.END)  # Limpiar el campo de entrada
        entry_marca.delete(0, tk.END)  # Limpiar el campo de entrada
        entry_tamaño.delete(0, tk.END)  # Limpiar el campo de entrada
        entry_tipo_entrada.delete(0, tk.END)  # Limpiar el campo de entrada
    else:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")

# Función para actualizar la tabla con datos de la base de datos
def actualizar_tabla():
    # Limpiar tabla
    for row in tabla.get_children():
        tabla.delete(row)

    # Obtener productos de la base de datos
    c.execute("SELECT id, nombre, descripcion, marca, tamaño, tipo_entrada FROM productos")
    productos = c.fetchall()

    # Insertar productos en la tabla
    for producto in productos:
        tabla.insert('', tk.END, values=(*producto, "..."))

# Crear ventana principal (Login)
ventana = tk.Tk()
ventana.title("Login")
ventana.geometry("600x400")
ventana.resizable(False, False)

# Configuración de fuentes y tamaños
font_large = ('Arial', 18)
font_medium = ('Arial', 14)

# Etiquetas y campos de entrada
label_usuario = tk.Label(ventana, text="Usuario:", font=font_large)
label_usuario.pack(pady=20)
entry_usuario = tk.Entry(ventana, font=font_medium, width=30)
entry_usuario.pack(pady=10)

label_contraseña = tk.Label(ventana, text="Contraseña:", font=font_large)
label_contraseña.pack(pady=20)
entry_contraseña = tk.Entry(ventana, show="*", font=font_medium, width=30)
entry_contraseña.pack(pady=10)

# Botón de login
boton_login = tk.Button(ventana, text="Iniciar sesión", font=font_large, command=verificar_login)
boton_login.pack(pady=30)

# Iniciar la aplicación
ventana.mainloop()

# Cerrar conexión a la base de datos cuando la aplicación termina
conn.close()
