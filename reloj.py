import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pytz
from datetime import datetime
import requests

# Traducciones para el clima
traducciones = {
    "Sunny": "Soleado",
    "Clear": "Despejado",
    "Partly cloudy": "Parcialmente nublado",
    "Cloudy": "Nublado",
    "Overcast": "Cubierto",
    "Light rain": "Lluvia ligera",
    "Patchy rain possible": "Posible lluvia dispersa",
    "Rain": "Lluvia",
    "Thunderstorm": "Tormenta",
    "Mist": "Niebla",
    "Fog": "Niebla",
    "Snow": "Nieve",
    "Light snow": "Nieve ligera",
    "Drizzle": "Llovizna",
    "Haze": "Calina",
    "Shower": "Chubasco"
}

# Obtener clima traducido desde wttr.in
def obtener_clima(ciudad):
    try:
        url = f"https://wttr.in/{ciudad}?format=%t+%C"
        resp = requests.get(url, timeout=3)
        if resp.status_code == 200:
            texto = resp.text.strip()
            partes = texto.split(" ", 1)
            temp = partes[0]
            desc = partes[1] if len(partes) > 1 else ""
            desc_esp = traducciones.get(desc, desc)
            return f"{temp} {desc_esp}"
        else:
            return "No disponible"
    except Exception:
        return "No disponible"

# Diccionario para las ciudades con al menos 10 entradas
CIUDADES = {
    "Buenos Aires": ("America/Argentina/Buenos_Aires", "buenos_aires.jpg"),
    "Nueva York": ("America/New_York", "nueva_york.jpg"),
    "Londres": ("Europe/London", "londres.jpg"),
    "Tokio": ("Asia/Tokyo", "tokio.jpg"),
    "Sídney": ("Australia/Sydney", "sidney.jpg"),
    "Ciudad del Cabo": ("Africa/Johannesburg", "ciudad_del_cabo.jpg"),
    "Los Ángeles": ("America/Los_Angeles", "los_angeles.jpg"),
    "París": ("Europe/Paris", "paris.jpg"),
    "Nueva Delhi": ("Asia/Kolkata", "nueva_delhi.jpg"),
    "Beijing": ("Asia/Shanghai", "beijing.jpg")
}

RUTA_IMAGENES = "imagenes/"

ventana = tk.Tk()
ventana.title("Reloj Mundial")
ventana.geometry("600x400")
ventana.resizable(False, False)

fondo_label = tk.Label(ventana)
fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

# Etiquetas centradas
frame_central = tk.Frame(ventana, bg="gray")
frame_central.place(relx=0.5, rely=0.4, anchor="center")

hora_label = tk.Label(frame_central, font=("Indie Flower", 40, "bold"), fg="white", bg="gray")
hora_label.pack(pady=(0, 5))

fecha_label = tk.Label(frame_central, font=("Indie Flower", 20), fg="white", bg="gray")
fecha_label.pack(pady=(0, 5))

clima_label = tk.Label(frame_central, font=("Indie Flower", 18), fg="white", bg="gray")
clima_label.pack(pady=(0, 10))

ciudad_var = tk.StringVar(value="Buenos Aires")
selector = ttk.Combobox(ventana, textvariable=ciudad_var, values=list(CIUDADES.keys()), state="readonly")
selector.pack(pady=(10, 0))

imagenes_cache = {}

def cargar_imagen(nombre_archivo, ancho, alto):
    if nombre_archivo in imagenes_cache:
        return imagenes_cache[nombre_archivo]
    ruta = RUTA_IMAGENES + nombre_archivo
    imagen = Image.open(ruta).resize((ancho, alto))
    imagen_tk = ImageTk.PhotoImage(imagen)
    imagenes_cache[nombre_archivo] = imagen_tk
    return imagen_tk

def actualizar():
    ciudad = ciudad_var.get()
    zona, fondo = CIUDADES[ciudad]
    zona_horaria = pytz.timezone(zona)
    ahora = datetime.now(zona_horaria)
    hora_str = ahora.strftime("%H:%M:%S")
    fecha_str = ahora.strftime("%A %d de %B de %Y")

    hora_label.config(text=hora_str)
    fecha_label.config(text=fecha_str.capitalize())

    clima = obtener_clima(ciudad)
    clima_label.config(text=f"Clima: {clima}")

    fondo_img = cargar_imagen(fondo, 600, 400)
    fondo_label.config(image=fondo_img)
    fondo_label.image = fondo_img

    ventana.after(1000, actualizar)

actualizar()
ventana.mainloop()
