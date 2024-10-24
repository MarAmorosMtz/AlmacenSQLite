import tkinter as tk
from tkinter import messagebox, ttk

# Función para verificar el login
def verificar_login():
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()

    if usuario == "admin" and contraseña == "1234":
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
    messagebox.showinfo("Editar", f"Editar entrada: {entrada}")

# Función para eliminar la entrada
def eliminar_entrada(item_id):
    confirmar = messagebox.askyesno("Eliminar", "¿Seguro que deseas eliminar esta entrada?")
    if confirmar:
        tabla.delete(item_id)

# Función para abrir la nueva ventana con la tabla
def abrir_nueva_ventana():
    global tabla

    nueva_ventana = tk.Tk()
    nueva_ventana.title("Dashboard")
    nueva_ventana.geometry("800x600")

    # Crear contenedor de pestañas
    tab_control = ttk.Notebook(nueva_ventana)
    tab_principal = ttk.Frame(tab_control)
    tab_opciones = ttk.Frame(tab_control)

    tab_control.add(tab_principal, text="Principal")
    tab_control.add(tab_opciones, text="Opciones")
    tab_control.pack(expand=1, fill='both')

    # ----- Pestaña Principal -----
    # Crear cuadro de búsqueda
    lbl_buscar = tk.Label(tab_principal, text="Buscar:")
    lbl_buscar.pack(pady=10)
    entry_buscar = tk.Entry(tab_principal, width=50)
    entry_buscar.pack(pady=10)

    # Crear tabla
    columnas = ("ID", "Nombre", "Marca", "Tamaño", "Cantidad", "Opciones")
    tabla = ttk.Treeview(tab_principal, columns=columnas, show="headings")
    tabla.heading("ID", text="ID")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Marca", text="Marca")
    tabla.heading("Tamaño", text="Tamaño")
    tabla.heading("Cantidad", text="Cantidad")
    tabla.heading("Opciones", text="Opciones")

    # Definir el ancho de las columnas
    tabla.column("ID", width=50)
    tabla.column("Nombre", width=150)
    tabla.column("Marca", width=100)
    tabla.column("Tamaño", width=100)
    tabla.column("Cantidad", width=100)
    tabla.column("Opciones", width=100)

    # Insertar datos ficticios en la tabla
    datos = [
        (1, "Laptop", "Dell", "15 pulgadas", 5),
        (2, "Monitor", "Samsung", "27 pulgadas", 10),
        (3, "Teclado", "Logitech", "Estándar", 25),
    ]

    for dato in datos:
        item_id = tabla.insert('', tk.END, values=(*dato, "..."))

    tabla.pack(pady=20, expand=True, fill='both')

    # Evento para detectar clic en la columna "Opciones"
    def on_click(event):
        # Obtener la posición del clic y el elemento seleccionado
        item_id = tabla.identify_row(event.y)
        column = tabla.identify_column(event.x)

        # Verificar si se hizo clic en la columna "Opciones" (que es la columna 6)
        if column == '#6' and item_id:
            mostrar_menu(event, item_id)

    # Vincular el evento clic a la tabla
    tabla.bind("<Button-1>", on_click)

    # ----- Pestaña de Opciones -----
    lbl_opciones = tk.Label(tab_opciones, text="Aquí puedes agregar más opciones", font=('Arial', 16))
    lbl_opciones.pack(pady=20)

    nueva_ventana.mainloop()

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
