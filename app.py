import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Conexión con la base de datos
conn = sqlite3.connect('store.db')
c = conn.cursor()

# Función para abrir la ventana de acceso
def ventana_acceso():
    nueva_ventana1 = tk.Tk()
    centrar_ventana(nueva_ventana1, 600, 400)
    nueva_ventana1.title("Acceso")
    tk.Label(nueva_ventana1, text="Acceder a:", font=("Arial", 16)).pack(pady=20)

    ttk.Button(nueva_ventana1, text="Consumibles", command=abrir_consumibles).pack(pady=10)
    ttk.Button(nueva_ventana1, text="Equipos", command=abrir_equipos).pack(pady=10)


# Función para abrir la ventana de Consumibles
def abrir_consumibles():
    global tabla
    global entry_cantidad, entry_nombre, entry_marca, entry_tamaño, entry_descripcion, entry_umed, entry_nota, entry_tag # Hacer accesibles los campos del formulario
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
    tk.Label(tab_principal, text="Buscar Consumible por Nombre:", font=('Arial', 12)).pack(pady=5)
    entry_busqueda = tk.Entry(tab_principal, font=('Arial', 12))
    entry_busqueda.pack(pady=5)

    # Crear un Frame para los botones
    frame_botones = tk.Frame(tab_principal)
    frame_botones.pack(pady=5)

    # Botón Buscar
    boton_buscar = tk.Button(frame_botones, text="Buscar", font=('Arial', 12), command=buscar_consumible)
    boton_buscar.pack(side=tk.LEFT, padx=(0, 10))  # Agrega un margen a la derecha

    # Botón Cancelar
    boton_cancelar = tk.Button(frame_botones, text="Cancelar", font=('Arial', 12), command=actualizar_tabla_consumibles)
    boton_cancelar.pack(side=tk.LEFT)

    # Crear tabla
    columnas = ("ID", "Nombre", "Descripción", "Marca", "Tamaño", "UMed", "Cantidad", "Nota", "Opciones")
    tabla = ttk.Treeview(tab_principal, columns=columnas, show="headings")
    tabla.heading("ID", text="ID")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Descripción", text="Descripción")
    tabla.heading("Marca", text="Marca")
    tabla.heading("Tamaño", text="Tamaño")
    tabla.heading("UMed", text="U. Med")
    tabla.heading("Cantidad", text="Cantidad")
    tabla.heading("Nota", text="Nota")
    tabla.heading("Opciones", text="Opciones")

    # Definir el ancho de las columnas
    tabla.column("ID", width=50)
    tabla.column("Nombre", width=150)
    tabla.column("Descripción", width=150)
    tabla.column("Marca", width=100)
    tabla.column("Tamaño", width=100)
    tabla.column("UMed", width=100)
    tabla.column("Cantidad", width=100)
    tabla.column("Nota", width=150)
    tabla.column("Opciones", width=100)

    tabla.pack(pady=20, expand=True, fill='both')

    # Evento para detectar clic en la columna "Opciones"
    def on_click(event):
        # Obtener la posición del clic y el elemento seleccionado
        item_id = tabla.identify_row(event.y)
        column = tabla.identify_column(event.x)

        # Verificar si se hizo clic en la columna "Opciones"
        if column == '#9' and item_id:
            mostrar_menu_consumible(event, item_id)

    # Vincular el evento clic a la tabla
    tabla.bind("<Button-1>", on_click)

    # Cargar datos de la base de datos en la tabla
    actualizar_tabla_consumibles()

    # ----- Pestaña de Opciones -----
    lbl_opciones = tk.Label(tab_opciones, text="Agregar Nuevos Consumibles", font=('Arial', 16))
    lbl_opciones.pack(pady=20)

    # Formulario para agregar nuevo consumible con etiquetas y campos en la misma fila, centrados

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

    # Unidad de medida
    fila_umed = tk.Frame(tab_opciones)
    fila_umed.pack(pady=5, anchor='center')
    tk.Label(fila_umed, text="Unidad de Medida:", font=('Arial', 14)).pack(side=tk.LEFT, padx=(0, 20))
    entry_umed = tk.Entry(fila_umed, font=('Arial', 14), width=30)
    entry_umed.pack(side=tk.LEFT)

    # Cantidad
    fila_cantidad = tk.Frame(tab_opciones)
    fila_cantidad.pack(pady=5, anchor='center')
    tk.Label(fila_cantidad, text="Cantidad:", font=('Arial', 14)).pack(side=tk.LEFT, padx=(0, 20))
    entry_cantidad = tk.Entry(fila_cantidad, font=('Arial', 14), width=30)
    entry_cantidad.pack(side=tk.LEFT)

    # Nota
    fila_nota = tk.Frame(tab_opciones)
    fila_nota.pack(pady=5, anchor='center')
    tk.Label(fila_nota, text="Nota:", font=('Arial', 14)).pack(side=tk.LEFT, padx=(0, 20))
    entry_nota = tk.Entry(fila_nota, font=('Arial', 14), width=30)
    entry_nota.pack(side=tk.LEFT)

    # Botón para agregar el consumible
    boton_agregar = tk.Button(tab_opciones, text="Agregar Consumible", font=('Arial', 14), command=agregar_consumible)
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

def abrir_equipos():
    global tabla
    global entry_tag, entry_cantidad, entry_nombre, entry_marca, entry_tamaño, entry_descripcion, entry_umed, entry_nota  # Hacer accesibles los campos del formulario
    global entry_busqueda

    nueva_ventana = tk.Tk()
    nueva_ventana.title("Dashboard")
    nueva_ventana.geometry("1300x800")

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
    tk.Label(tab_principal, text="Buscar Equipo por Nombre:", font=('Arial', 12)).pack(pady=5)
    entry_busqueda = tk.Entry(tab_principal, font=('Arial', 12))
    entry_busqueda.pack(pady=5)

    # Crear un Frame para los botones
    frame_botones = tk.Frame(tab_principal)
    frame_botones.pack(pady=5)

    # Botón Buscar
    boton_buscar = tk.Button(frame_botones, text="Buscar", font=('Arial', 12), command=buscar_equipo)
    boton_buscar.pack(side=tk.LEFT, padx=(0, 10))  # Agrega un margen a la derecha

    # Botón Cancelar
    boton_cancelar = tk.Button(frame_botones, text="Cancelar", font=('Arial', 12), command=actualizar_tabla_equipos)
    boton_cancelar.pack(side=tk.LEFT)

    # Crear tabla
    columnas = ("ID", "Tag", "Nombre", "Descripción", "Marca", "Tamaño", "UMed", "Cantidad", "Nota", "Opciones")
    tabla = ttk.Treeview(tab_principal, columns=columnas, show="headings")
    tabla.heading("ID", text="ID")
    tabla.heading("Tag", text="Tag")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Descripción", text="Descripción")
    tabla.heading("Marca", text="Marca")
    tabla.heading("Tamaño", text="Tamaño")
    tabla.heading("UMed", text="U. Med")
    tabla.heading("Cantidad", text="Cantidad")
    tabla.heading("Nota", text="Nota")
    tabla.heading("Opciones", text="Opciones")

    # Definir el ancho de las columnas
    tabla.column("ID", width=50)
    tabla.column("Tag", width=100)
    tabla.column("Nombre", width=150)
    tabla.column("Descripción", width=150)
    tabla.column("Marca", width=100)
    tabla.column("Tamaño", width=100)
    tabla.column("UMed", width=100)
    tabla.column("Cantidad", width=100)
    tabla.column("Nota", width=150)
    tabla.column("Opciones", width=100)

    tabla.pack(pady=20, expand=True, fill='both')

    # Evento para detectar clic en la columna "Opciones"
    def on_click(event):
        # Obtener la posición del clic y el elemento seleccionado
        item_id = tabla.identify_row(event.y)
        column = tabla.identify_column(event.x)

        # Verificar si se hizo clic en la columna "Opciones"
        if column == '#10' and item_id:
            mostrar_menu_equipo(event, item_id)

    # Vincular el evento clic a la tabla
    tabla.bind("<Button-1>", on_click)

    # Cargar datos de la base de datos en la tabla
    actualizar_tabla_equipos()

    # ----- Pestaña de Opciones -----
    lbl_opciones = tk.Label(tab_opciones, text="Agregar Nuevos Equipos", font=('Arial', 16))
    lbl_opciones.pack(pady=20)

    # Formulario para agregar nuevo equipo con etiquetas y campos en la misma fila, centrados
    fila_tag = tk.Frame(tab_opciones)
    fila_tag.pack(pady=5, anchor='center')
    tk.Label(fila_tag, text="Tag:", font=('Arial', 14)).pack(side=tk.LEFT, padx=(0, 20))
    entry_tag = tk.Entry(fila_tag, font=('Arial', 14), width=30)
    entry_tag.pack(side=tk.LEFT)

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

    # Unidad de medida
    fila_umed = tk.Frame(tab_opciones)
    fila_umed.pack(pady=5, anchor='center')
    tk.Label(fila_umed, text="Unidad de Medida:", font=('Arial', 14)).pack(side=tk.LEFT, padx=(0, 20))
    entry_umed = tk.Entry(fila_umed, font=('Arial', 14), width=30)
    entry_umed.pack(side=tk.LEFT)

    # Cantidad
    fila_cantidad = tk.Frame(tab_opciones)
    fila_cantidad.pack(pady=5, anchor='center')
    tk.Label(fila_cantidad, text="Cantidad:", font=('Arial', 14)).pack(side=tk.LEFT, padx=(0, 20))
    entry_cantidad = tk.Entry(fila_cantidad, font=('Arial', 14), width=30)
    entry_cantidad.pack(side=tk.LEFT)

    # Nota
    fila_nota = tk.Frame(tab_opciones)
    fila_nota.pack(pady=5, anchor='center')
    tk.Label(fila_nota, text="Nota:", font=('Arial', 14)).pack(side=tk.LEFT, padx=(0, 20))
    entry_nota = tk.Entry(fila_nota, font=('Arial', 14), width=30)
    entry_nota.pack(side=tk.LEFT)

    # Botón para agregar el equipo
    boton_agregar = tk.Button(tab_opciones, text="Agregar Equipo", font=('Arial', 14), command=agregar_equipo)
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
        rol = rol_usuario.get()
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

    nueva_ventana.mainloop()




# Función para verificar el login
def verificar_login():
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()

    # Verificar credenciales en la base de datos
    c.execute("SELECT rol FROM usuarios WHERE nombre=? AND pass=?", (usuario, contraseña))
    result = c.fetchone()

    if result:
        global rol_usuario  # Declarar la variable global
        rol_usuario = result[0]  # Almacenar el rol
        ventana.destroy()
        ventana_acceso()  # Abrir ventana de acceso
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")


# Función para mostrar el menú de opciones (editar/eliminar)
def mostrar_menu_consumible(event, item_id):
    menu = tk.Menu(tabla, tearoff=0)
    menu.add_command(label="Editar", command=lambda: editar_entrada_consumible(item_id))
    menu.add_command(label="Eliminar", command=lambda: eliminar_entrada_consumible(item_id))
    menu.post(event.x_root, event.y_root)

# Función para editar la entrada
def editar_entrada_consumible(item_id):
    entrada = tabla.item(item_id)['values']
    abrir_ventana_editar_consumible(entrada)

# Función para abrir la ventana de edición
def abrir_ventana_editar_consumible(entrada):
    def actualizar_consumible():
        nuevo_nombre = entry_nombre.get()
        nueva_descripcion = entry_descripcion.get("1.0", tk.END).strip()
        nueva_marca = entry_marca.get()
        nuevo_tamaño = entry_tamaño.get()
        nueva_umed = entry_umed.get()
        nueva_cantidad = entry_cantidad.get()
        nueva_nota = entry_nota.get()

        if nuevo_nombre and nueva_descripcion and nueva_marca and nuevo_tamaño and nueva_umed and nueva_cantidad:
            c.execute("""UPDATE consumibles 
                         SET nombre=?, descripcion=?, marca=?, tamaño=?, umed=?, cantidad=?, nota=? 
                         WHERE id=?""",
                      (nuevo_nombre, nueva_descripcion, nueva_marca, nuevo_tamaño, nueva_umed, nueva_cantidad, nueva_nota, entrada[0]))
            conn.commit()
            messagebox.showinfo("Actualizar Consumible", "Consumible actualizado correctamente.")
            actualizar_tabla_consumibles()
            editar_ventana.destroy()  # Cerrar ventana de edición
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")

    editar_ventana = tk.Toplevel()
    editar_ventana.title("Editar Consumible")
    centrar_ventana(editar_ventana, 600, 600)

    # Formulario para editar consumible
    # Nombre
    fila_nombre = tk.Frame(editar_ventana)
    fila_nombre.pack(pady=5, anchor='center')
    tk.Label(fila_nombre, text="Nombre:", font=('Arial', 14)).pack(side=tk.LEFT, padx=(0, 20))
    entry_nombre = tk.Entry(fila_nombre, font=('Arial', 14), width=30)
    entry_nombre.pack(side=tk.LEFT)
    entry_nombre.insert(0, entrada[1])

    # Descripción
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

    # Unidad de Medida
    fila_umed = tk.Frame(editar_ventana)
    fila_umed.pack(pady=5, anchor='center')
    tk.Label(fila_umed, text="Unidad de Medida:", font=('Arial', 14)).pack(side=tk.LEFT, padx=(0, 20))
    entry_umed = tk.Entry(fila_umed, font=('Arial', 14), width=30)
    entry_umed.pack(side=tk.LEFT)
    entry_umed.insert(0, entrada[5])

    # Cantidad
    fila_cantidad = tk.Frame(editar_ventana)
    fila_cantidad.pack(pady=5, anchor='center')
    tk.Label(fila_cantidad, text="Cantidad:", font=('Arial', 14)).pack(side=tk.LEFT, padx=(0, 20))
    entry_cantidad = tk.Entry(fila_cantidad, font=('Arial', 14), width=30)
    entry_cantidad.pack(side=tk.LEFT)
    entry_cantidad.insert(0, entrada[6])

    # Nota
    fila_nota = tk.Frame(editar_ventana)
    fila_nota.pack(pady=5, anchor='center')
    tk.Label(fila_nota, text="Nota:", font=('Arial', 14)).pack(side=tk.LEFT, padx=(0, 20))
    entry_nota = tk.Entry(fila_nota, font=('Arial', 14), width=30)
    entry_nota.pack(side=tk.LEFT)
    entry_nota.insert(0, entrada[7])

    # Contenedor de los botones de actualización y cancelación
    fila_botones = tk.Frame(editar_ventana)
    fila_botones.pack(pady=20, anchor='center')

    # Botón de actualizar
    boton_actualizar = tk.Button(fila_botones, text="Actualizar", font=('Arial', 12), command=actualizar_consumible)
    boton_actualizar.pack(side=tk.LEFT, padx=(0, 20))

    # Botón de cancelar
    boton_cancelar = tk.Button(fila_botones, text="Cancelar", font=('Arial', 12), command=editar_ventana.destroy)
    boton_cancelar.pack(side=tk.LEFT)


# Función para eliminar la entrada
def eliminar_entrada_consumible(item_id):
    entrada = tabla.item(item_id)['values']
    confirmar = messagebox.askyesno("Eliminar", f"¿Seguro que deseas eliminar el producto {entrada[1]}?")
    if confirmar:
        # Eliminar de la base de datos
        c.execute("DELETE FROM consumibles WHERE id=?", (entrada[0],))
        conn.commit()
        actualizar_tabla_consumibles()

# Función para agregar un producto a la base de datos
import tkinter as tk
from tkinter import messagebox

def agregar_consumible():
    nombre = entry_nombre.get()
    descripcion = entry_descripcion.get("1.0", tk.END).strip()
    marca = entry_marca.get()
    tamaño = entry_tamaño.get()
    umed = entry_umed.get()
    cantidad = entry_cantidad.get()
    nota = entry_nota.get()

    if nombre and descripcion and marca and tamaño and umed and cantidad:
        c.execute("INSERT INTO consumibles (nombre, descripcion, marca, tamaño, umed, cantidad, nota) VALUES (?, ?, ?, ?, ?, ?, ?) ",
                  (nombre, descripcion, marca, tamaño, umed, cantidad, nota))
        conn.commit()
        messagebox.showinfo("Agregar Consumible", "Consumible agregado correctamente.")
        actualizar_tabla_consumibles()  # Actualizar la tabla si existe una función para ello

        # Limpiar entradas
        entry_nombre.delete(0, tk.END)
        entry_descripcion.delete("1.0", tk.END)
        entry_marca.delete(0, tk.END)
        entry_tamaño.delete(0, tk.END)
        entry_umed.delete(0, tk.END)
        entry_cantidad.delete(0, tk.END)
        entry_nota.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")

def agregar_equipo():
    tag = entry_tag.get()  # Obtener el valor del campo 'tag'
    nombre = entry_nombre.get()
    descripcion = entry_descripcion.get("1.0", tk.END).strip()
    marca = entry_marca.get()
    tamaño = entry_tamaño.get()
    umed = entry_umed.get()
    cantidad = entry_cantidad.get()
    nota = entry_nota.get()

    if tag and nombre and descripcion and marca and tamaño and umed and cantidad:  # Verificar que todos los campos estén completos
        # Insertar los datos en la base de datos
        c.execute(""" 
        INSERT INTO equipos (tag, nombre, descripcion, marca, tamaño, umed, cantidad, nota) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?) 
        """, (tag, nombre, descripcion, marca, tamaño, umed, cantidad, nota))
        conn.commit()
        messagebox.showinfo("Agregar Equipo", "Equipo agregado correctamente.")
        actualizar_tabla_equipos()  # Actualizar la tabla si existe una función para ello

        # Limpiar entradas
        entry_tag.delete(0, tk.END)  # Limpiar el campo 'tag'
        entry_nombre.delete(0, tk.END)
        entry_descripcion.delete("1.0", tk.END)
        entry_marca.delete(0, tk.END)
        entry_tamaño.delete(0, tk.END)
        entry_umed.delete(0, tk.END)
        entry_cantidad.delete(0, tk.END)
        entry_nota.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")



# Funcionamiento del cuadro de busqueda, se ejecuta al presionar el boton "Buscar"
def buscar_consumible():
    nombre = entry_busqueda.get()
    for row in tabla.get_children():
        tabla.delete(row)

    # Realizar la búsqueda en la base de datos
    c.execute("SELECT * FROM consumibles WHERE nombre LIKE ?", ('%' + nombre + '%',))
    consumibles = c.fetchall()

    # Insertar consumibles en la tabla
    for consumible in consumibles:
        tabla.insert('', tk.END, values=(*consumible, "..."))


def buscar_equipo():
    nombre = entry_busqueda.get()
    for row in tabla.get_children():
        tabla.delete(row)

    # Realizar la búsqueda en la base de datos
    c.execute("SELECT * FROM equipos WHERE nombre LIKE ?", ('%' + nombre + '%',))
    equipos = c.fetchall()

    # Insertar equipos en la tabla
    for equipo in equipos:
        tabla.insert('', tk.END, values=(*equipo, "..."))


# Función para actualizar la tabla con datos de la base de datos
def actualizar_tabla_consumibles():
    # Limpiar tabla
    for row in tabla.get_children():
        tabla.delete(row)

    # Obtener consumibles de la base de datos
    c.execute("SELECT * FROM consumibles")
    consumibles = c.fetchall()

    # Insertar consumibles en la tabla
    for consumible in consumibles:
        tabla.insert('', tk.END, values=(*consumible, "..."))  # Agregar "..." o algún valor adicional si es necesario

    entry_busqueda.delete(0, tk.END)  # Limpiar campo de búsqueda si existe

def actualizar_tabla_equipos():
    # Limpiar tabla
    for row in tabla.get_children():
        tabla.delete(row)

    # Obtener equipos de la base de datos
    c.execute("SELECT * FROM equipos")
    equipos = c.fetchall()

    # Insertar equipos en la tabla
    for equipo in equipos:
        tabla.insert('', tk.END, values=(*equipo, "..."))  # Agregar "..." o algún valor adicional si es necesario

    entry_busqueda.delete(0, tk.END)  # Limpiar campo de búsqueda si existe


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

# Función para abrir la ventana de edición del equipo
def abrir_ventana_editar_equipo(entrada):
    def actualizar_equipo():
        nuevo_tag = entry_tag.get()
        nuevo_nombre = entry_nombre.get()
        nueva_descripcion = entry_descripcion.get("1.0", tk.END).strip()
        nueva_marca = entry_marca.get()
        nuevo_tamaño = entry_tamaño.get()
        nueva_umed = entry_umed.get()
        nueva_cantidad = entry_cantidad.get()
        nueva_nota = entry_nota.get()

        if nuevo_tag and nuevo_nombre and nueva_descripcion and nueva_marca and nuevo_tamaño and nueva_umed and nueva_cantidad:
            c.execute("""UPDATE equipos 
                         SET tag=?, nombre=?, descripcion=?, marca=?, tamaño=?, umed=?, cantidad=?, nota=? 
                         WHERE id=?""",
                      (nuevo_tag, nuevo_nombre, nueva_descripcion, nueva_marca, nuevo_tamaño, nueva_umed, nueva_cantidad, nueva_nota, entrada[0]))
            conn.commit()
            messagebox.showinfo("Actualizar Equipo", "Equipo actualizado correctamente.")
            actualizar_tabla_equipos()
            editar_ventana.destroy()  # Cerrar ventana de edición
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")

    editar_ventana = tk.Toplevel()
    editar_ventana.title("Editar Equipo")
    centrar_ventana(editar_ventana, 600, 600)

    # Formulario para editar equipo
    # Tag
    fila_tag = tk.Frame(editar_ventana)
    fila_tag.pack(pady=5, anchor='center')
    tk.Label(fila_tag, text="Tag:", font=('Arial', 14)).pack(side=tk.LEFT, padx=(0, 20))
    entry_tag = tk.Entry(fila_tag, font=('Arial', 14), width=30)
    entry_tag.pack(side=tk.LEFT)
    entry_tag.insert(0, entrada[1])  # Asignar el valor actual

    # Nombre
    fila_nombre = tk.Frame(editar_ventana)
    fila_nombre.pack(pady=5, anchor='center')
    tk.Label(fila_nombre, text="Nombre:", font=('Arial', 14)).pack(side=tk.LEFT, padx=(0, 20))
    entry_nombre = tk.Entry(fila_nombre, font=('Arial', 14), width=30)
    entry_nombre.pack(side=tk.LEFT)
    entry_nombre.insert(0, entrada[2])  # Asignar el valor actual

    # Descripción
    fila_descripcion = tk.Frame(editar_ventana)
    fila_descripcion.pack(pady=5, anchor='center')
    tk.Label(fila_descripcion, text="Descripción:", font=('Arial', 14)).pack(side=tk.LEFT, padx=(0, 20))
    entry_descripcion = tk.Text(fila_descripcion, font=('Arial', 14), width=30, height=4)
    entry_descripcion.pack(side=tk.LEFT)
    entry_descripcion.insert("1.0", entrada[3])  # Asignar el valor actual

    # Marca
    fila_marca = tk.Frame(editar_ventana)
    fila_marca.pack(pady=5, anchor='center')
    tk.Label(fila_marca, text="Marca:", font=('Arial', 14)).pack(side=tk.LEFT, padx=(0, 20))
    entry_marca = tk.Entry(fila_marca, font=('Arial', 14), width=30)
    entry_marca.pack(side=tk.LEFT)
    entry_marca.insert(0, entrada[4])  # Asignar el valor actual

    # Tamaño
    fila_tamaño = tk.Frame(editar_ventana)
    fila_tamaño.pack(pady=5, anchor='center')
    tk.Label(fila_tamaño, text="Tamaño:", font=('Arial', 14)).pack(side=tk.LEFT, padx=(0, 20))
    entry_tamaño = tk.Entry(fila_tamaño, font=('Arial', 14), width=30)
    entry_tamaño.pack(side=tk.LEFT)
    entry_tamaño.insert(0, entrada[5])  # Asignar el valor actual

    # Unidad de Medida
    fila_umed = tk.Frame(editar_ventana)
    fila_umed.pack(pady=5, anchor='center')
    tk.Label(fila_umed, text="Unidad de Medida:", font=('Arial', 14)).pack(side=tk.LEFT, padx=(0, 20))
    entry_umed = tk.Entry(fila_umed, font=('Arial', 14), width=30)
    entry_umed.pack(side=tk.LEFT)
    entry_umed.insert(0, entrada[6])  # Asignar el valor actual

    # Cantidad
    fila_cantidad = tk.Frame(editar_ventana)
    fila_cantidad.pack(pady=5, anchor='center')
    tk.Label(fila_cantidad, text="Cantidad:", font=('Arial', 14)).pack(side=tk.LEFT, padx=(0, 20))
    entry_cantidad = tk.Entry(fila_cantidad, font=('Arial', 14), width=30)
    entry_cantidad.pack(side=tk.LEFT)
    entry_cantidad.insert(0, entrada[7])  # Asignar el valor actual

    # Nota
    fila_nota = tk.Frame(editar_ventana)
    fila_nota.pack(pady=5, anchor='center')
    tk.Label(fila_nota, text="Nota:", font=('Arial', 14)).pack(side=tk.LEFT, padx=(0, 20))
    entry_nota = tk.Entry(fila_nota, font=('Arial', 14), width=30)
    entry_nota.pack(side=tk.LEFT)
    entry_nota.insert(0, entrada[8])  # Asignar el valor actual

    # Contenedor de los botones de actualización y cancelación
    fila_botones = tk.Frame(editar_ventana)
    fila_botones.pack(pady=20, anchor='center')

    # Botón de actualizar
    boton_actualizar = tk.Button(fila_botones, text="Actualizar", font=('Arial', 12), command=actualizar_equipo)
    boton_actualizar.pack(side=tk.LEFT, padx=(0, 20))

    # Botón de cancelar
    boton_cancelar = tk.Button(fila_botones, text="Cancelar", font=('Arial', 12), command=editar_ventana.destroy)
    boton_cancelar.pack(side=tk.LEFT)


def actualizar_tabla_equipos():
    # Limpiar tabla
    for row in tabla.get_children():
        tabla.delete(row)

    # Obtener equipos de la base de datos
    c.execute("SELECT * FROM equipos")
    equipos = c.fetchall()

    # Insertar equipos en la tabla
    for equipo in equipos:
        tabla.insert('', tk.END, values=(*equipo, "..."))  # Agregar "..." o algún valor adicional si es necesario

    entry_busqueda.delete(0, tk.END)  # Limpiar campo de búsqueda si existe

def buscar_equipo():
    nombre = entry_busqueda.get()
    for row in tabla.get_children():
        tabla.delete(row)

    # Realizar la búsqueda en la base de datos
    c.execute("SELECT * FROM equipos WHERE nombre LIKE ?", ('%' + nombre + '%',))
    equipos = c.fetchall()

    # Insertar equipos en la tabla
    for equipo in equipos:
        tabla.insert('', tk.END, values=(*equipo, "..."))

# Función para mostrar el menú de opciones (editar/eliminar)
def mostrar_menu_equipo(event, item_id):
    menu = tk.Menu(tabla, tearoff=0)
    menu.add_command(label="Editar", command=lambda: editar_entrada_equipo(item_id))
    menu.add_command(label="Eliminar", command=lambda: eliminar_entrada_equipo(item_id))
    menu.post(event.x_root, event.y_root)

# Función para editar la entrada
def editar_entrada_equipo(item_id):
    entrada = tabla.item(item_id)['values']
    abrir_ventana_editar_equipo(entrada)

# Función para eliminar la entrada
def eliminar_entrada_equipo(item_id):
    # Confirmar antes de eliminar
    if messagebox.askyesno("Eliminar", "¿Estás seguro de que deseas eliminar este equipo?"):
        equipo_id = tabla.item(item_id)["values"][0]  # Obtener el ID del equipo
        c.execute("DELETE FROM equipos WHERE id = ?", (equipo_id,))
        conn.commit()
        actualizar_tabla_equipos()  # Actualizar la tabla después de eliminar

# Función para abrir la ventana de edición de equipo
def abrir_ventana_editar_equipo(entrada):
    ventana_editar = tk.Toplevel()
    ventana_editar.title("Editar Equipo")
    ventana_editar.geometry("400x400")

    # Crear campos de entrada para los datos del equipo
    tk.Label(ventana_editar, text="Nombre:").pack()
    entry_nombre_edit = tk.Entry(ventana_editar)
    entry_nombre_edit.insert(0, entrada[2])  # Nombre
    entry_nombre_edit.pack()

    tk.Label(ventana_editar, text="Descripción:").pack()
    entry_descripcion_edit = tk.Entry(ventana_editar)
    entry_descripcion_edit.insert(0, entrada[3])  # Descripción
    entry_descripcion_edit.pack()

    tk.Label(ventana_editar, text="Marca:").pack()
    entry_marca_edit = tk.Entry(ventana_editar)
    entry_marca_edit.insert(0, entrada[4])  # Marca
    entry_marca_edit.pack()

    tk.Label(ventana_editar, text="Tamaño:").pack()
    entry_tamaño_edit = tk.Entry(ventana_editar)
    entry_tamaño_edit.insert(0, entrada[5])  # Tamaño
    entry_tamaño_edit.pack()

    tk.Label(ventana_editar, text="Unidad de Medida:").pack()
    entry_umed_edit = tk.Entry(ventana_editar)
    entry_umed_edit.insert(0, entrada[6])  # Unidad de Medida
    entry_umed_edit.pack()

    tk.Label(ventana_editar, text="Cantidad:").pack()
    entry_cantidad_edit = tk.Entry(ventana_editar)
    entry_cantidad_edit.insert(0, entrada[7])  # Cantidad
    entry_cantidad_edit.pack()

    tk.Label(ventana_editar, text="Nota:").pack()
    entry_nota_edit = tk.Entry(ventana_editar)
    entry_nota_edit.insert(0, entrada[8])  # Nota
    entry_nota_edit.pack()

    # Botón para guardar los cambios
    def guardar_cambios():
        equipo_id = entrada[0]  # Obtener ID del equipo para actualizar
        nuevo_nombre = entry_nombre_edit.get()
        nueva_descripcion = entry_descripcion_edit.get()
        nueva_marca = entry_marca_edit.get()
        nuevo_tamaño = entry_tamaño_edit.get()
        nueva_umed = entry_umed_edit.get()
        nueva_cantidad = entry_cantidad_edit.get()
        nueva_nota = entry_nota_edit.get()

        # Actualizar los datos en la base de datos
        c.execute("""
        UPDATE equipos
        SET nombre = ?, descripcion = ?, marca = ?, tamaño = ?, umed = ?, cantidad = ?, nota = ?
        WHERE id = ?
        """, (nuevo_nombre, nueva_descripcion, nueva_marca, nuevo_tamaño, nueva_umed, nueva_cantidad, nueva_nota, equipo_id))
        conn.commit()
        actualizar_tabla_equipos()  # Actualizar la tabla después de editar
        ventana_editar.destroy()  # Cerrar la ventana de edición

    tk.Button(ventana_editar, text="Guardar Cambios", command=guardar_cambios).pack(pady=20)


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
