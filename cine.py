import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Importar ttk para estilos avanzados
from PIL import Image, ImageTk

# Configuración inicial de la ventana principal
root = tk.Tk()
root.title("Aplicación de Reserva de Asientos de Cine")
root.geometry("1000x900")
root.configure(bg='#2b2b2b')

# Variables globales
salas = ["Sala 1", "Sala 2", "Sala 3"]
peliculas = ["Película 1", "Película 2", "Película 3"]
horarios = ["10:00 AM", "4:00 PM"]

# Estructura para mantener el estado de los asientos en cada sala y horario por película
estado_asientos = {}
for sala in salas:
    estado_asientos[sala] = {}
    for pelicula in peliculas:
        estado_asientos[sala][pelicula] = {}
        for horario in horarios:
            estado_asientos[sala][pelicula][horario] = [["L" for _ in range(5)] for _ in range(5)]

# Lista para almacenar los asientos seleccionados
asientos_seleccionados = []

# Funciones
def seleccionar_pelicula():
    sala = sala_var.get()
    pelicula = pelicula_var.get()
    horario = horario_var.get()
    if pelicula and horario and sala:
        mostrar_asientos(pelicula, horario)
    else:
        messagebox.showwarning("Advertencia", "Seleccione una película, horario y sala")

def mostrar_asientos(pelicula, horario):
    for widget in asiento_frame.winfo_children():
        widget.destroy()
    
    asientos = estado_asientos[sala_var.get()][pelicula][horario]
    
    for i, fila in enumerate(asientos):
        for j, asiento in enumerate(fila):
            color = "green" if asiento == "L" else "red" if asiento == "O" else "yellow" if asiento == "S" else "white"
            btn = tk.Button(asiento_frame, text=asiento, bg=color, font=("Arial", 14), command=lambda i=i, j=j: seleccionar_asiento(i, j, pelicula, horario))
            btn.grid(row=i, column=j, padx=5, pady=5)

def seleccionar_asiento(fila, columna, pelicula, horario):
    asientos = estado_asientos[sala_var.get()][pelicula][horario]
    if asientos[fila][columna] == "L":
        asientos[fila][columna] = "S"
        asientos_seleccionados.append((fila, columna))
    elif asientos[fila][columna] == "S":
        asientos[fila][columna] = "L"
        asientos_seleccionados.remove((fila, columna))
    mostrar_asientos(pelicula, horario)

def reservar_asiento():
    pelicula = pelicula_var.get()
    horario = horario_var.get()
    if not asientos_seleccionados:
        messagebox.showwarning("Advertencia", "Seleccione al menos un asiento")
        return

    for fila, columna in asientos_seleccionados:
        asientos = estado_asientos[sala_var.get()][pelicula][horario]
        if asientos[fila][columna] == "S":
            asientos[fila][columna] = "O"

    asientos_seleccionados.clear()
    mostrar_asientos(pelicula, horario)
    messagebox.showinfo("Reserva", "Asientos seleccionados reservados con éxito")

def marcar_mejores_asientos():
    pelicula = pelicula_var.get()
    horario = horario_var.get()
    asientos = estado_asientos[sala_var.get()][pelicula][horario]

    # Verificar si hay asientos libres en la primera fila
    if 'L' in asientos[0]:
        for i, asiento in enumerate(asientos[0]):
            if asiento == "L" and asientos[0][i] != "O":
                btn = asiento_frame.grid_slaves(row=0, column=i)[0]
                btn.configure(bg="blue")
        return

    messagebox.showinfo("Mejores Asientos", "Todos los mejores asientos están ocupados.")

# Interfaz gráfica
pelicula_var = tk.StringVar()
horario_var = tk.StringVar()
sala_var = tk.StringVar()

# Cargar imágenes
img1 = Image.open("imagen1.png")
img1 = img1.resize((150, 200), Image.LANCZOS)
img1 = ImageTk.PhotoImage(img1)

img2 = Image.open("imagen2.png")
img2 = img2.resize((150, 200), Image.LANCZOS)
img2 = ImageTk.PhotoImage(img2)

img3 = Image.open("imagen3.png")
img3 = img3.resize((150, 200), Image.LANCZOS)
img3 = ImageTk.PhotoImage(img3)

# Diccionario para asociar películas con imágenes
imagenes_peliculas = {
    "Película 1": img1,
    "Película 2": img2,
    "Película 3": img3
}

# Frame para las películas
peliculas_frame = tk.Frame(root, bg='#2b2b2b')
peliculas_frame.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.Y)

# Mostrar imágenes de las películas en forma vertical
for pelicula in peliculas:
    frame = tk.Frame(peliculas_frame, bg='#2b2b2b')
    frame.pack(pady=5)
    label = tk.Label(frame, text=pelicula, bg='#2b2b2b', fg='white', font=("Arial", 12))
    label.pack()
    img_label = tk.Label(frame, image=imagenes_peliculas[pelicula])
    img_label.pack()
    rb = tk.Radiobutton(frame, variable=pelicula_var, value=pelicula)
    rb.pack()

# Frame para los horarios
horarios_frame = tk.Frame(root, bg='#2b2b2b')
horarios_frame.pack(pady=5)

tk.Label(horarios_frame, text="Seleccione un horario:", bg='#2b2b2b', fg='white', font=("Arial", 12)).pack(pady=5)
for horario in horarios:
    tk.Radiobutton(horarios_frame, text=horario, variable=horario_var, value=horario).pack(anchor=tk.CENTER)

# Frame para las salas
salas_frame = tk.Frame(root, bg='#2b2b2b')
salas_frame.pack(pady=5)

tk.Label(salas_frame, text="Seleccione una sala:", bg='#2b2b2b', fg='white', font=("Arial", 12)).pack(pady=5)
for sala in salas:
    tk.Radiobutton(salas_frame, text=sala, variable=sala_var, value=sala).pack(anchor=tk.CENTER)

# Botón para mostrar los asientos
tk.Button(root, text="Mostrar asientos", command=seleccionar_pelicula, bg='#3c3c3c', fg='white', font=("Arial", 14)).pack(pady=10)

# Frame para los asientos
asiento_frame = tk.Frame(root, bg='#2b2b2b')
asiento_frame.pack(pady=10)

# Botón para marcar los mejores asientos
tk.Button(root, text="Mostrar Mejores Asientos", command=marcar_mejores_asientos, bg='#3c3c3c', fg='white', font=("Arial", 14)).pack(pady=5)

# Botón para reservar asientos seleccionados
tk.Button(root, text="Reservar Asiento", command=reservar_asiento, bg='#3c3c3c', fg='white', font=("Arial", 14)).pack(pady=5)

# Ejecutar la aplicación
root.mainloop()
