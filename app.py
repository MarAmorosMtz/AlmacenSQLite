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
    c.execute("SELECT rol FROM usuarios WHERE nombre=? AND pass=?", (usuario, contraseña))
    result = c.fetchone()

    if result:
        global rol_usuario  # Declarar la variable global
        rol_usuario = result[0]  # Almacenar el rol
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
        nueva_descripcion = entry_descripcion.get("1.0", tk.END).strip()
        nueva_marca = entry_marca.get()
        nuevo_tamaño = entry_tamaño.get()
        nuevo_tipo_entrada = entry_tipo_entrada.get()
        nueva_cantidad = entry_cantidad.get()

        if nuevo_nombre and nueva_descripcion and nueva_marca and nuevo_tamaño and nuevo_tipo_entrada:
            c.execute("UPDATE productos SET nombre=?, descripcion=?, marca=?, tamaño=?, tipo_entrada=?, cantidad=? WHERE id=?",
                      (nuevo_nombre, nueva_descripcion, nueva_marca, nuevo_tamaño, nuevo_tipo_entrada, nueva_cantidad, entrada[0]))
            conn.commit()
            messagebox.showinfo("Actualizar Producto", "Producto actualizado correctamente.")
            actualizar_tabla()
            editar_ventana.destroy()  # Cerrar ventana de edición
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")

    editar_ventana = tk.Toplevel()
    editar_ventana.title("Editar Producto")
    centrar_ventana(editar_ventana, 600, 600)

    # Formulario para agregar nuevo producto con etiquetas y campos en la misma fila, centrados
    # Nombre
    fila_nombre = tk.Frame(editar_ventana)
    fila_nombre.pack(pady=5, anchor='center')
    tk.Label(fila_nombre, text="Nombre:", font=('Arial', 14)).pack(side=tk.LEFT, padx=(0, 20))
    entry_nombre = tk.Entry(fila_nombre, font=('Arial', 14), width=30)
    entry_nombre.pack(side=tk.LEFT)
    entry_nombre.insert(0, entrada[1])

    # Descripción como área de texto (Text)
    fila_descripcion = tk.Frame(editar_ventana)
    fila_descripcion.pack(pady=5, anchor='center')
    tk.Label(fila_descripcion, text="Descripción:", font=('Arial', 14)).pack(side=tk.LEFT, padx=(0, 20))
    entry_descripcion = tk.Text(fila_descripcion, font=('Arial', 14), width=30, height=4)
    entry_descripcion.pack(side=tk.LEFT)
    entry_descripcion.insert("1.0", entrada[2])

    # Marca
    fila_marca = tk.Frame(editar_ventana)
    fila_marca.pack(pady=5, anchor='center')
    tk.Label(fila_marca, text="Marca:", font=('Arial', 14)).pack(side=tk.LEFT, padx=(0, 20))
    entry_marca = tk.Entry(fila_marca, font=('Arial', 14), width=30)
    entry_marca.pack(side=tk.LEFT)
    entry_marca.insert(0, entrada[3])

    # Tamaño
    fila_tamaño = tk.Frame(editar_ventana)
    fila_tamaño.pack(pady=5, anchor='center')
    tk.Label(fila_tamaño, text="Tamaño:", font=('Arial', 14)).pack(side=tk.LEFT, padx=(0, 20))
    entry_tamaño = tk.Entry(fila_tamaño, font=('Arial', 14), width=30)
    entry_tamaño.pack(side=tk.LEFT)
    entry_tamaño.insert(0, entrada[4])

    # Tipo de Entrada
    fila_tipo_entrada = tk.Frame(editar_ventana)
    fila_tipo_entrada.pack(pady=5, anchor='center')
    tk.Label(fila_tipo_entrada, text="Tipo de Entrada:", font=('Arial', 14)).pack(side=tk.LEFT, padx=(0, 20))
    entry_tipo_entrada = tk.Entry(fila_tipo_entrada, font=('Arial', 14), width=30)
    entry_tipo_entrada.pack(side=tk.LEFT)
    entry_tipo_entrada.insert(0, entrada[5])

    # Cantidad
    fila_cantidad = tk.Frame(editar_ventana)
    fila_cantidad.pack(pady=5, anchor='center')
    tk.Label(fila_cantidad, text="Cantidad:", font=('Arial', 14)).pack(side=tk.LEFT, padx=(0, 20))
    entry_cantidad = tk.Entry(fila_cantidad, font=('Arial', 14), width=30)
    entry_cantidad.pack(side=tk.LEFT)
    entry_cantidad.insert(0, entrada[6])

    # Contenedor de los botones de actualización y cancelación centrado
    fila_botones = tk.Frame(editar_ventana)
    fila_botones.pack(pady=20, anchor='center')  # Centra el contenedor de botones

    # Botón de actualizar
    boton_actualizar = tk.Button(fila_botones, text="Actualizar", font=('Arial', 12), command=actualizar_producto)
    boton_actualizar.pack(side=tk.LEFT, padx=(0, 20))

    # Botón de cancelar
    boton_cancelar = tk.Button(fila_botones, text="Cancelar", font=('Arial', 12), command=editar_ventana.destroy)
    boton_cancelar.pack(side=tk.LEFT)


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
    global entry_cantidad, entry_nombre, entry_marca, entry_tamaño, entry_descripcion, entry_tipo_entrada  # Hacer accesibles los campos del formulario
    global entry_busqueda

    nueva_ventana = tk.Tk()
    nueva_ventana.title("Dashboard")
    nueva_ventana.geometry("1000x800")

    # Crear contenedor de pestañas
    tab_control = ttk.Notebook(nueva_ventana)
    tab_principal = ttk.Frame(tab_control)
    tab_opciones = ttk.Frame(tab_control)
    tab_agregarUsuario = ttk.Frame(tab_control)

    tab_control.add(tab_principal, text="Principal")
    tab_control.add(tab_opciones, text="Agregar Producto")

    # Solo añadir la pestaña de agregar usuario si el rol es admin
    if rol_usuario == 'admin':
        tab_control.add(tab_agregarUsuario, text="Agregar Usuario")

    tab_control.pack(expand=1, fill='both')

    # ----- Pestaña Principal -----

    # Cuadro de búsqueda y botón
    tk.Label(tab_principal, text="Buscar Producto por Nombre:", font=('Arial', 12)).pack(pady=5)
    entry_busqueda = tk.Entry(tab_principal, font=('Arial', 12))
    entry_busqueda.pack(pady=5)

    # Crear un Frame para los botones
    frame_botones = tk.Frame(tab_principal)
    frame_botones.pack(pady=5)

    # Botón Buscar
    boton_buscar = tk.Button(frame_botones, text="Buscar", font=('Arial', 12), command=buscar_producto)
    boton_buscar.pack(side=tk.LEFT, padx=(0, 10))  # Agrega un margen a la derecha

    # Botón Cancelar
    boton_cancelar = tk.Button(frame_botones, text="Cancelar", font=('Arial', 12), command=actualizar_tabla)
    boton_cancelar.pack(side=tk.LEFT)  # No necesita margen a la izquierda

    # Crear tabla
    columnas = ("ID", "Nombre", "Descripción", "Marca", "Tamaño", "Tipo de Entrada", "Cantidad", "Opciones")
    tabla = ttk.Treeview(tab_principal, columns=columnas, show="headings")
    tabla.heading("ID", text="ID")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Descripción", text="Descripción")
    tabla.heading("Marca", text="Marca")
    tabla.heading("Tamaño", text="Tamaño")
    tabla.heading("Tipo de Entrada", text="Tipo de Entrada")
    tabla.heading("Cantidad", text="Cantidad")
    tabla.heading("Opciones", text="Opciones")

    # Definir el ancho de las columnas
    tabla.column("ID", width=50)
    tabla.column("Nombre", width=150)
    tabla.column("Descripción", width=150)
    tabla.column("Marca", width=100)
    tabla.column("Tamaño", width=100)
    tabla.column("Tipo de Entrada", width=100)
    tabla.column("Cantidad", width=100)
    tabla.column("Opciones", width=100)

    tabla.pack(pady=20, expand=True, fill='both')

    # Evento para detectar clic en la columna "Opciones"
    def on_click(event):
        # Obtener la posición del clic y el elemento seleccionado
        item_id = tabla.identify_row(event.y)
        column = tabla.identify_column(event.x)

        # Verificar si se hizo clic en la columna "Opciones"
        if column == '#8' and item_id:
            mostrar_menu(event, item_id)

    # Vincular el evento clic a la tabla
    tabla.bind("<Button-1>", on_click)

    # Cargar datos de la base de datos en la tabla
    actualizar_tabla()

    # ----- Pestaña de Opciones -----
    lbl_opciones = tk.Label(tab_opciones, text="Agregar Nuevos Productos", font=('Arial', 16))
    lbl_opciones.pack(pady=20)

    # Formulario para agregar nuevo producto con etiquetas y campos en la misma fila, centrados
    # Nombre
    fila_nombre = tk.Frame(tab_opciones)
    fila_nombre.pack(pady=5, anchor='center')
    tk.Label(fila_nombre, text="Nombre:", font=('Arial', 14)).pack(side=tk.LEFT, padx=(0, 20))
    entry_nombre = tk.Entry(fila_nombre, font=('Arial', 14), width=30)
    entry_nombre.pack(side=tk.LEFT)

    # Descripción como área de texto (Text)
    fila_descripcion = tk.Frame(tab_opciones)
    fila_descripcion.pack(pady=5, anchor='center')
    tk.Label(fila_descripcion, text="Descripción:", font=('Arial', 14)).pack(side=tk.LEFT, padx=(0, 20))
    entry_descripcion = tk.Text(fila_descripcion, font=('Arial', 14), width=30, height=4)
    entry_descripcion.pack(side=tk.LEFT)

    # Marca
    fila_marca = tk.Frame(tab_opciones)
    fila_marca.pack(pady=5, anchor='center')
    tk.Label(fila_marca, text="Marca:", font=('Arial', 14)).pack(side=tk.LEFT, padx=(0, 20))
    entry_marca = tk.Entry(fila_marca, font=('Arial', 14), width=30)
    entry_marca.pack(side=tk.LEFT)

    # Tamaño
    fila_tamaño = tk.Frame(tab_opciones)
    fila_tamaño.pack(pady=5, anchor='center')
    tk.Label(fila_tamaño, text="Tamaño:", font=('Arial', 14)).pack(side=tk.LEFT, padx=(0, 20))
    entry_tamaño = tk.Entry(fila_tamaño, font=('Arial', 14), width=30)
    entry_tamaño.pack(side=tk.LEFT)

    # Tipo de Entrada
    fila_tipo_entrada = tk.Frame(tab_opciones)
    fila_tipo_entrada.pack(pady=5, anchor='center')
    tk.Label(fila_tipo_entrada, text="Tipo de Entrada:", font=('Arial', 14)).pack(side=tk.LEFT, padx=(0, 20))
    entry_tipo_entrada = tk.Entry(fila_tipo_entrada, font=('Arial', 14), width=30)
    entry_tipo_entrada.pack(side=tk.LEFT)

    # Cantidad
    fila_cantidad = tk.Frame(tab_opciones)
    fila_cantidad.pack(pady=5, anchor='center')
    tk.Label(fila_cantidad, text="Cantidad:", font=('Arial', 14)).pack(side=tk.LEFT, padx=(0, 20))
    entry_cantidad = tk.Entry(fila_cantidad, font=('Arial', 14), width=30)
    entry_cantidad.pack(side=tk.LEFT)

    # Botón para agregar el producto
    boton_agregar = tk.Button(tab_opciones, text="Agregar Producto", font=('Arial', 14), command=agregar_producto)
    boton_agregar.pack(pady=20)

    # ----- Pestaña Agregar Usuario -----
    lbl_agregar_usuario = tk.Label(tab_agregarUsuario, text="Crear Nuevo Usuario", font=('Arial', 16))
    lbl_agregar_usuario.pack(pady=20)

    # Usuario
    fila_usuario = tk.Frame(tab_agregarUsuario)
    fila_usuario.pack(pady=5, anchor='center')
    tk.Label(fila_usuario, text="Usuario:", font=('Arial', 14)).pack(side=tk.LEFT, padx=(0, 20))
    entry_usuario = tk.Entry(fila_usuario, font=('Arial', 14), width=30)
    entry_usuario.pack(side=tk.LEFT)

    # Contraseña
    fila_contraseña = tk.Frame(tab_agregarUsuario)
    fila_contraseña.pack(pady=5, anchor='center')
    tk.Label(fila_contraseña, text="Contraseña:", font=('Arial', 14)).pack(side=tk.LEFT, padx=(0, 20))
    entry_contraseña = tk.Entry(fila_contraseña, font=('Arial', 14), show="*", width=30)
    entry_contraseña.pack(side=tk.LEFT)

    # Rol
    fila_rol = tk.Frame(tab_agregarUsuario)
    fila_rol.pack(pady=5, anchor='center')
    tk.Label(fila_rol, text="Rol:", font=('Arial', 14)).pack(side=tk.LEFT, padx=(0, 20))

    rol_var = tk.StringVar(value="general")
    radio_admin = tk.Radiobutton(fila_rol, text="Administrador", variable=rol_var, value="admin", font=('Arial', 12))
    radio_general = tk.Radiobutton(fila_rol, text="General", variable=rol_var, value="general", font=('Arial', 12))
    radio_admin.pack(side=tk.LEFT, padx=(0, 10))
    radio_general.pack(side=tk.LEFT)

    # Función para agregar usuario
    def agregar_usuario():
        usuario = entry_usuario.get()
        password = entry_contraseña.get()
        rol = rol_var.get()
        if usuario and password:
            c.execute("INSERT INTO usuarios (nombre, pass, rol) VALUES (?, ?, ?)", (usuario, password, rol))
            conn.commit()
            messagebox.showinfo("Agregar Usuario", "Usuario agregado correctamente.")

            # Limpiar entradas
            entry_usuario.delete(0, tk.END)
            entry_contraseña.delete(0, tk.END)

            actualizar_tabla_usuarios()

    # Botón para agregar el usuario
    boton_agregar_usuario = tk.Button(tab_agregarUsuario, text="Agregar Usuario", font=('Arial', 14),
                                      command=agregar_usuario)
    boton_agregar_usuario.pack(pady=20)

    # ----- Tabla de Usuarios -----
    columnas_usuarios = ("Usuario", "Rol", "Acciones")
    tabla_usuarios = ttk.Treeview(tab_agregarUsuario, columns=columnas_usuarios, show="headings")
    tabla_usuarios.heading("Usuario", text="Usuario")
    tabla_usuarios.heading("Rol", text="Rol")
    tabla_usuarios.heading("Acciones", text="Eliminar")

    # Definir el ancho de las columnas
    tabla_usuarios.column("Usuario", width=150)
    tabla_usuarios.column("Rol", width=100)
    tabla_usuarios.column("Acciones", width=100)

    tabla_usuarios.pack(pady=20, expand=True, fill='both')

    # Función para actualizar la tabla de usuarios
    def actualizar_tabla_usuarios():
        # Limpiar la tabla
        for item in tabla_usuarios.get_children():
            tabla_usuarios.delete(item)

        # Cargar datos de la base de datos en la tabla
        c.execute("SELECT nombre, rol FROM usuarios")
        usuarios = c.fetchall()
        for usuario in usuarios:
            tabla_usuarios.insert("", tk.END, values=(usuario[0], usuario[1], "Eliminar"))

    # Evento para detectar clic en la columna "Acciones"
    def on_click_usuarios(event):
        item_id = tabla_usuarios.identify_row(event.y)
        column = tabla_usuarios.identify_column(event.x)

        # Verificar si se hizo clic en la columna "Acciones"
        if column == '#3' and item_id:
            eliminar_usuario(item_id)

    # Vincular el evento clic a la tabla de usuarios
    tabla_usuarios.bind("<Button-1>", on_click_usuarios)

    # Función para eliminar un usuario
    def eliminar_usuario(item_id):
        usuario = tabla_usuarios.item(item_id, 'values')[0]
        confirm = messagebox.askyesno("Eliminar Usuario", f"¿Estás seguro de que deseas eliminar a '{usuario}'?")
        if confirm:
            c.execute("DELETE FROM usuarios WHERE nombre=?", (usuario,))
            conn.commit()
            messagebox.showinfo("Eliminar Usuario", "Usuario eliminado correctamente.")
            actualizar_tabla_usuarios()  # Actualizar la tabla después de eliminar

    # Cargar la tabla de usuarios al iniciar
    actualizar_tabla_usuarios()

    nueva_ventana.mainloop()

# Función para agregar un producto a la base de datos
def agregar_producto():
    nombre = entry_nombre.get()
    descripcion = entry_descripcion.get("1.0", tk.END).strip()
    marca = entry_marca.get()
    tamaño = entry_tamaño.get()
    tipo_entrada = entry_tipo_entrada.get()
    cantidad = entry_cantidad.get()

    if nombre and descripcion and marca and tamaño and tipo_entrada:
        c.execute("INSERT INTO productos (nombre, descripcion, marca, tamaño, tipo_entrada, cantidad) VALUES (?, ?, ?, ?, ?, ?)",
                  (nombre, descripcion, marca, tamaño, tipo_entrada, cantidad))
        conn.commit()
        messagebox.showinfo("Agregar Producto", "Producto agregado correctamente.")
        actualizar_tabla()

        #Limpiar entradas
        entry_nombre.delete(0, tk.END)
        entry_descripcion.delete("1.0", tk.END)
        entry_marca.delete(0, tk.END)
        entry_tamaño.delete(0, tk.END)
        entry_tipo_entrada.delete(0, tk.END)
        entry_cantidad.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")

# Funcionamiento del cuadro de busqueda, se ejecuta al presionar el boton "Buscar"
def buscar_producto():
    nombre = entry_busqueda.get()
    for row in tabla.get_children():
        tabla.delete(row)

    # Realizar la búsqueda en la base de datos
    c.execute("SELECT * FROM productos WHERE nombre LIKE ?", ('%' + nombre + '%',))
    productos = c.fetchall()

    # Insertar productos en la tabla
    for producto in productos:
        tabla.insert('', tk.END, values=(*producto, "..."))

# Función para actualizar la tabla con datos de la base de datos
def actualizar_tabla():
    # Limpiar tabla
    for row in tabla.get_children():
        tabla.delete(row)

    # Obtener productos de la base de datos
    c.execute("SELECT * FROM productos")
    productos = c.fetchall()

    # Insertar productos en la tabla
    for producto in productos:
        tabla.insert('', tk.END, values=(*producto, "..."))

    entry_busqueda.delete(0, tk.END)

# Función para centrar una ventana
def centrar_ventana(ventana, ancho, alto):
    # Obtener el tamaño de la pantalla
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    # Calcular la posición x e y
    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2)
    # Establecer la geometría de la ventana
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

# Crear ventana principal (Login)
ventana = tk.Tk()
ventana.title("Login")
centrar_ventana(ventana, 600, 400)
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
