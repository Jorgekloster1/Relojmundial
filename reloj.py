import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pytz
from datetime import datetime
import requests
import random
import json
import os
import threading
from tkinter import font

# --- Configuración y Datos (mantener igual) ---
RUTA_IMAGENES = "imagenes/"

COLORES = {
    "fondo_principal": "#2c3e50", # Azul oscuro para fondos principales
    "fondo_secundario": "#34495e", # Azul ligeramente más claro para fondos secundarios/modales
    "texto_claro": "#ecf0f1",      # Blanco roto para texto sobre fondos oscuros
    "texto_oscuro": "#34495e",     # Azul oscuro para texto sobre fondos claros (botones, combobox)
    "acento_principal": "#3498db", # Azul brillante para elementos interactivos/destacados
    "acento_secundario": "#2980b9", # Azul más oscuro para estados activos
    "borde": "#95a5a6",            # Gris medio para bordes (si se usan)
    "exito": "#27ae60",            # Verde para mensajes de éxito
    "error": "#c0392b"             # Rojo para mensajes de error
}

traducciones = {
    "Sunny": "Soleado", "Clear": "Despejado", "Partly cloudy": "Parcialmente nublado",
    "Cloudy": "Nublado", "Overcast": "Cubierto", "Light rain": "Lluvia ligera",
    "Patchy rain possible": "Posible lluvia dispersa", "Rain": "Lluvia", "Thunderstorm": "Tormenta",
    "Mist": "Niebla", "Fog": "Niebla", "Snow": "Nieve", "Light snow": "Nieve ligera",
    "Drizzle": "Llovizna", "Haze": "Calina", "Shower": "Chubasco",
    "Heavy rain": "Lluvia intensa", "Moderate rain": "Lluvia moderada",
    "Freezing fog": "Niebla helada", "Blizzard": "Ventisca",
    "Light drizzle": "Llovizna ligera", "Moderate or heavy rain shower": "Chubasco moderado o fuerte",
    "Heavy snow": "Nieve pesada", "Patchy light drizzle": "Llovizna ligera dispersa",
    "Patchy moderate snow": "Nieve moderada dispersa", "Patchy heavy snow": "Nieve pesada dispersa",
    "Patchy sleet possible": "Posible aguanieve dispersa", "Light showers of ice pellets": "Ligeros chubascos de gránulos de hielo",
    "Patchy freezing drizzle possible": "Posible llovizna helada dispersa", "Thundery outbreaks in nearby": "Tormentas en las cercanías",
    "Torrential rain shower": "Chubasco de lluvia torrencial", "Blustery": "Ventoso",
    "Patchy snow possible": "Posible nieve dispersa"
}

dias_es = {
    "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles",
    "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"
}
meses_es = {
    "January": "enero", "February": "febrero", "March": "marzo", "April": "abril",
    "May": "mayo", "June": "junio", "July": "julio", "August": "agosto",
    "September": "septiembre", "October": "octubre", "November": "noviembre", "December": "diciembre"
}

def traducir_fecha(fecha_str):
    """Traduce una cadena de fecha del inglés al español."""
    for en, es in dias_es.items():
        fecha_str = fecha_str.replace(en, es)
    for en, es in meses_es.items():
        fecha_str = fecha_str.replace(en, es)
    return fecha_str

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

PAISES = {
    "Buenos Aires": "Argentina", "Nueva York": "Estados Unidos", "Londres": "Reino Unido",
    "Tokio": "Japón", "Sídney": "Australia", "Ciudad del Cabo": "Sudáfrica",
    "Los Ángeles": "Estados Unidos", "París": "Francia", "Nueva Delhi": "India",
    "Beijing": "China"
}

preguntas = {
    "Argentina": [
        {"pregunta": "¿Qué invento se originó en Argentina?", "opciones": ["El colectivo", "La televisión", "El subte", "El microondas"], "respuesta": "El colectivo"},
        {"pregunta": "¿Cuándo fue la Revolución de Mayo?", "opciones": ["25 de mayo de 1810", "9 de julio de 1816", "2 de abril de 1982", "20 de junio"], "respuesta": "25 de mayo de 1810"},
        {"pregunta": "¿Qué baile tradicional es famoso en Argentina?", "opciones": ["Samba", "Tango", "Cumbia", "Salsa"], "respuesta": "Tango"},
        {"pregunta": "¿Quién compuso 'La Cumparsita', uno de los tangos más famosos?", "opciones": ["Carlos Gardel", "Astor Piazzolla", "Gerardo Matos Rodríguez", "Aníbal Troilo"], "respuesta": "Gerardo Matos Rodríguez"},
        {"pregunta": "¿En qué año Argentina ganó su primer Mundial de Fútbol?", "opciones": ["1970", "1978", "1986", "2022"], "respuesta": "1978"}
    ],
    "Japón": [
        {"pregunta": "¿Qué significa 'Konnichiwa'?", "opciones": ["Gracias", "Hola", "Buenas tardes", "Adiós"], "respuesta": "Buenas tardes"},
        {"pregunta": "¿Qué ocurrió el 6 de agosto de 1945?", "opciones": ["Inicio de la era Reiwa", "Terremoto de Tōhoku", "Bomba en Hiroshima", "Festival de las muñecas"], "respuesta": "Bomba en Hiroshima"},
        {"pregunta": "¿Qué montaña es un símbolo de Japón?", "opciones": ["Monte Everest", "Monte Fuji", "Monte Kilimanjaro", "Monte Blanco"], "respuesta": "Monte Fuji"},
        {"pregunta": "¿Cuál es la capital de Japón?", "opciones": ["Kioto", "Osaka", "Tokio", "Nagoya"], "respuesta": "Tokio"},
        {"pregunta": "¿Qué tipo de flor es famosa en Japón y se asocia con la primavera?", "opciones": ["Rosa", "Girasol", "Sakura", "Tulipán"], "respuesta": "Sakura"}
    ],
    "Reino Unido": [
        {"pregunta": "¿Cuál es la residencia oficial de la monarquía británica en Londres?", "opciones": ["Torre de Londres", "Palacio de Buckingham", "Castillo de Windsor", "Palacio de Westminster"], "respuesta": "Palacio de Buckingham"},
        {"pregunta": "¿Qué famoso grupo musical se formó en Liverpool?", "opciones": ["Rolling Stones", "Queen", "The Beatles", "Led Zeppelin"], "respuesta": "The Beatles"},
        {"pregunta": "¿Cuál es el río principal que atraviesa Londres?", "opciones": ["Río Severn", "Río Támesis", "Río Clyde", "Río Tyne"], "respuesta": "Río Támesis"}
    ],
    "Estados Unidos": [
        {"pregunta": "¿Cuál es el río más largo de Estados Unidos?", "opciones": ["Río Colorado", "Río Misisipi", "Río Columbia", "Río Hudson"], "respuesta": "Río Misisipi"},
        {"pregunta": "¿En qué ciudad se encuentra la Estatua de la Libertad?", "opciones": ["Washington D.C.", "Los Ángeles", "Chicago", "Nueva York"], "respuesta": "Nueva York"},
        {"pregunta": "¿Cuál es la bebida no alcohólica más consumida en EE.UU.?", "opciones": ["Café", "Jugo de naranja", "Gaseosa", "Té"], "respuesta": "Gaseosa"}
    ],
    "Francia": [
        {"pregunta": "¿Qué famoso monumento se encuentra en París?", "opciones": ["Coliseo", "Estatua de la Libertad", "Torre Eiffel", "Big Ben"], "respuesta": "Torre Eiffel"},
        {"pregunta": "¿Cuál es el famoso museo de arte en París que alberga la Mona Lisa?", "opciones": ["Museo Británico", "Museo del Prado", "Museo del Louvre", "Galería Uffizi"], "respuesta": "Museo del Louvre"},
        {"pregunta": "¿Cuál es la famosa carrera ciclista que se celebra anualmente en Francia?", "opciones": ["Vuelta a España", "Giro de Italia", "Tour de Francia", "París-Roubaix"], "respuesta": "Tour de Francia"}
    ],
    "Australia": [
        {"pregunta": "¿Qué animal marsupial es emblemático de Australia?", "opciones": ["Koala", "Oso Panda", "Mono", "Llama"], "respuesta": "Koala"},
        {"pregunta": "¿Cuál es la capital de Australia?", "opciones": ["Sídney", "Melbourne", "Canberra", "Brisbane"], "respuesta": "Canberra"},
        {"pregunta": "¿Cuál es el famoso edificio con forma de velas en Sídney?", "opciones": ["Opera House", "Tower Bridge", "Burj Khalifa", "Coliseo"], "respuesta": "Opera House"}
    ],
    "India": [
        {"pregunta": "¿Qué monumento en la India es una de las Siete Maravillas del Mundo?", "opciones": ["Gran Muralla China", "Torre de Pisa", "Taj Mahal", "Pirámides de Giza"], "respuesta": "Taj Mahal"},
        {"pregunta": "¿Quién fue un líder pacifista clave en la independencia de la India?", "opciones": ["Jawaharlal Nehru", "Indira Gandhi", "Mahatma Gandhi", "Sardar Patel"], "respuesta": "Mahatma Gandhi"},
        {"pregunta": "¿Cuál es el festival de colores que se celebra en India?", "opciones": ["Diwali", "Eid", "Holi", "Navratri"], "respuesta": "Holi"}
    ],
    "Sudáfrica": [
        {"pregunta": "¿Quién fue el primer presidente de Sudáfrica elegido democráticamente?", "opciones": ["Desmond Tutu", "F.W. de Klerk", "Nelson Mandela", "Thabo Mbeki"], "respuesta": "Nelson Mandela"},
        {"pregunta": "¿Qué ciudad es conocida como la 'Ciudad Madre' de Sudáfrica?", "opciones": ["Johannesburgo", "Durban", "Ciudad del Cabo", "Pretoria"], "respuesta": "Ciudad del Cabo"},
        {"pregunta": "¿Cuál es el nombre del famoso parque nacional en Sudáfrica conocido por su vida salvaje?", "opciones": ["Serengueti", "Masai Mara", "Kruger", "Etosha"], "respuesta": "Kruger"}
    ],
    "China": [
        {"pregunta": "¿Cuál es la capital de China?", "opciones": ["Shanghái", "Hong Kong", "Pekín", "Cantón"], "respuesta": "Pekín"},
        {"pregunta": "¿Cuál es la estructura defensiva más larga del mundo, ubicada en China?", "opciones": ["Gran Muralla China", "Muro de Adriano", "Línea Maginot", "Muralla de Constantinopla"], "respuesta": "Gran Muralla China"},
        {"pregunta": "¿Qué animal, símbolo de China, es conocido por alimentarse casi exclusivamente de bambú?", "opciones": ["Tigre", "Oso pardo", "Panda gigante", "Dragón"], "respuesta": "Panda gigante"}
    ]
}

datos_curiosos = {
    "Argentina": ["Argentina tiene más psicólogos por habitante que cualquier otro país.", "El tango se originó en Buenos Aires.", "La Avenida 9 de Julio es una de las más anchas del mundo.", "El colectivo fue inventado en Argentina.", "Maradona es considerado una leyenda del fútbol argentino."],
    "Estados Unidos": ["EE.UU. no tiene idioma oficial a nivel federal.", "El Gran Cañón puede verse desde el espacio.", "La Estatua de la Libertad fue un regalo de Francia.", "Hollywood es la capital del cine mundial.", "EE.UU. tiene la economía más grande del mundo."],
    "Reino Unido": ["Big Ben es el nombre de la campana, no del reloj.", "Londres tiene más de 170 museos.", "El Reino Unido está compuesto por 4 naciones.", "El metro de Londres es el más antiguo del mundo.", "Se conduce por la izquierda."],
    "Japón": ["Hay más mascotas que niños en Japón.", "El sushi no siempre lleva pescado crudo.", "El Monte Fuji es un volcán activo.", "Los trenes son extremadamente puntuales.", "Tokio es la ciudad más poblada del mundo."],
    "Australia": ["Hay más canguros que personas en Australia.", "La Gran Barrera de Coral es el mayor arrecife del mundo.", "Hay más de 10,000 playas en Australia.", "Australia exporta vino a más de 100 países.", "Tiene una de las tasas más altas de rayos UV."],
    "Sudáfrica": ["Tiene 11 idiomas oficiales.", "Es el único país con 3 capitales.", "Aquí nació Nelson Mandela.", "Tiene el 'Table Mountain', una de las 7 maravillas naturales.", "Es hogar del 'Big Five' en vida salvaje."],
    "Francia": ["Es el país más visitado del mundo.", "Tiene más de 400 tipos de queso.", "París se llama la 'Ciudad de la Luz'.", "Francia fue pionera en los derechos humanos.", "Inventores del cine: los Hermanos Lumière."],
    "India": ["Produce más películas que cualquier otro país.", "El sistema decimal fue inventado aquí.", "El yoga nació en la India.", "Tiene la segunda población más grande del mundo.", "Usan más de 20 idiomas oficiales."],
    "China": ["La Muralla China tiene más de 21,000 km.", "El papel fue inventado en China.", "Tiene más de 1,400 millones de habitantes.", "El Año Nuevo Chino cambia cada año.", "Inventaron la pólvora, brújula y seda."]
}

datos_frases = {
    "Argentina": ["Che, ¿cómo estás? – Saludo informal muy usado entre amigos.", "Es un quilombo – Algo muy desordenado o complicado.", "Tengo fiaca – Tengo pereza o ganas de no hacer nada.", "Nos vemos, cuidate – Despedida amistosa.", "¿Todo bien? – Forma común de preguntar cómo estás."],
    "Estados Unidos": ["What's up? – ¿Qué tal? / ¿Qué pasa?", "Take it easy – Tómatelo con calma.", "No worries – No hay problema.", "Catch you later – Te veo luego.", "How's it going? – ¿Cómo va todo?"],
    "Reino Unido": ["Cheers! – Gracias o brindis.", "Fancy a cuppa? – ¿Querés una taza de té?", "Mate – Amigo, colega.", "Brilliant! – ¡Genial!", "I'm knackered – Estoy agotado."],
    "Japón": ["こんにちは (Konnichiwa) – Buenas tardes.", "ありがとう (Arigatou) – Gracias.", "すみません (Sumimasen) – Disculpe/perdón.", "さようなら (Sayonara) – Adiós.", "おはよう (Ohayou) – Buenos días."],
    "Australia": ["G'day mate – Hola amigo.", "No worries – Está todo bien.", "Fair dinkum – En serio / de verdad.", "She'll be right – Todo saldrá bien.", "Arvo – Tarde (forma corta de afternoon)."],
    "Sudáfrica": ["Howzit? – ¿Cómo estás?", "Just now – En un rato (aunque puede ser mucho después).", "Braai – Asado.", "Lekker – Genial / sabroso.", "Robot – Semáforo."],
    "Francia": ["Bonjour – Buen día.", "Merci – Gracias.", "Ça va? – ¿Todo bien?", "S'il vous plaît – Por favor.", "Au revoir – Adiós."],
    "India": ["Namaste – Saludo tradicional (hola/adiós).", "Achha – Bien / de acuerdo.", "Shukriya – Gracias.", "Bas – Basta / suficiente.", "Thik hai – Está bien / ok."],
    "China": ["你好 (Nǐ hǎo) – Hola.", "谢谢 (Xièxiè) – Gracias.", "没关系 (Méi guānxi) – No hay problema.", "再见 (Zàijiàn) – Adiós.", "好的 (Hǎo de) – Está bien / ok."]
}

datos_eventos = {
    "Argentina": ["25 de mayo de 1810: Revolución de Mayo.", "9 de julio de 1816: Declaración de la Independencia.", "2 de abril: Día de los Caídos en Malvinas.", "20 de junio: Día de la Bandera.", "17 de octubre de 1945: Día de la Lealtad."],
    "Estados Unidos": ["4 de julio de 1776: Declaración de la Independencia.", "11 de septiembre de 2001: Atentado a las Torres Gemelas.", "20 de julio de 1969: Primeros humanos en la Luna.", "1 de enero de 1863: Proclamación de Emancipación.", "14 de abril de 1865: Asesinatos de Lincoln."],
    "Reino Unido": ["5 de noviembre de 1605: Conspiración de la pólvora.", "2 de junio de 1953: Coronación de la Reina Isabel II.", "23 de junio de 2016: Referéndum del Brexit.", "18 de junio de 1815: Derrota de Napoleón en Waterloo.", "25 de diciembre de 1066: Coronación de Guillermo el Conquistador."],
    "Japón": ["6 de agosto de 1945: Bombardeo atómico de Hiroshima.", "11 de marzo de 2011: Gran Terremoto y Tsunami de Tohoku.", "1 de mayo de 2019: Inicio de la era Reiwa.", "3 de marzo: Hinamatsuri (Festival de las Niñas).", "15 de agosto de 1945: Rendición de Japón en la Segunda Guerra Mundial."],
    "Australia": ["1 de enero de 1901: Federación de Australia.", "26 de enero: Día de Australia (controversia).", "25 de abril: Día de ANZAC (Día de los Veteranos).", "1967: Referéndum que otorga derechos a los aborígenes.", "2000: Juegos Olímpicos de Sídney."],
    "Sudáfrica": ["27 de abril de 1994: Primeras elecciones democráticas multirraciales.", "11 de febrero de 1990: Liberación de Nelson Mandela.", "31 de mayo de 1961: Establecimiento de la República de Sudáfrica.", "1995: Sudáfrica gana la Copa Mundial de Rugby.", "1996: Adopción de la nueva Constitución democrática."],
    "Francia": ["14 de julio de 1789: Toma de la Bastilla (Revolución Francesa).", "1804: Napoleón Bonaparte se corona Emperador de los franceses.", "1944: Liberación de París de la ocupación nazi.", "1889: Inauguración de la Torre Eiffel.", "1900: Exposición Universal de París."],
    "India": ["15 de agosto de 1947: Independencia del Reino Unido.", "26 de enero de 1950: Entrada en vigor de la Constitución india (Día de la República).", "2 de octubre: Nacimiento de Mahatma Gandhi (Día de la No Violencia).", "2008: Atentados terroristas en Bombay.", "2014: Elección de Narendra Modi como Primer Ministro."],
    "China": ["1 de octubre de 1949: Proclamación de la República Popular China.", "4 de junio de 1989: Incidentes de la Plaza de Tiananmén.", "1978: Inicio de las reformas económicas de Deng Xiaoping.", "2008: Juegos Olímpicos de Verano en Beijing.", "2020: Cierre por COVID-19 en Wuhan."]
}

# --- Sistema de Progreso de Trivia ---
progreso = {}

def cargar_progreso():
    """Carga el progreso de trivia desde 'progreso.json'."""
    global progreso
    if os.path.exists("progreso.json"):
        try:
            with open("progreso.json", "r", encoding="utf-8") as f:
                progreso = json.load(f)
        except json.JSONDecodeError:
            messagebox.showwarning("Error de Carga", "El archivo de progreso está corrupto. Se iniciará un nuevo progreso.")
            progreso = {}
    else:
        progreso = {}

def guardar_progreso():
    """Guarda el progreso actual de trivia en 'progreso.json'."""
    with open("progreso.json", "w", encoding="utf-8") as f:
        json.dump(progreso, f, indent=4)

def registrar_respuesta_correcta(pais, indice_pregunta):
    """Registra una pregunta como correctamente respondida para un país."""
    if pais not in progreso:
        progreso[pais] = {"preguntas_correctas": []}
    if indice_pregunta not in progreso[pais]["preguntas_correctas"]:
        progreso[pais]["preguntas_correctas"].append(indice_pregunta)
        guardar_progreso()

def calcular_porcentaje(pais):
    """Calcula el porcentaje de preguntas correctas para un país específico."""
    total = len(preguntas.get(pais, []))
    correctas = len(progreso.get(pais, {}).get("preguntas_correctas", []))
    # Evitar división por cero si no hay preguntas para el país
    return round((correctas / total) * 100) if total else 0

def calcular_progreso_global():
    """Calcula el porcentaje de preguntas correctas a nivel global."""
    total_preguntas_global = 0
    aciertos_global = 0
    for pais in preguntas:
        total_preguntas_global += len(preguntas[pais])
        aciertos_global += len(progreso.get(pais, {}).get("preguntas_correctas", []))
    # Evitar división por cero si no hay preguntas globales
    return round((aciertos_global / total_preguntas_global) * 100) if total_preguntas_global else 0

# --- Carga de Imágenes ---
imagenes_cache = {}

def cargar_imagen(nombre_archivo, ancho, alto):
    """
    Carga y redimensiona una imagen para usarla como fondo.
    Utiliza un caché para optimizar el rendimiento.
    """
    ruta = os.path.join(RUTA_IMAGENES, nombre_archivo)
    if not os.path.exists(ruta):
        print(f"Error: No se encontró la imagen en {ruta}")
        return None
    
    cache_key = (nombre_archivo, ancho, alto)
    if cache_key in imagenes_cache:
        return imagenes_cache[cache_key]
    
    try:
        imagen = Image.open(ruta).resize((ancho, alto), Image.LANCZOS)
        imagen_tk = ImageTk.PhotoImage(imagen)
        imagenes_cache[cache_key] = imagen_tk
        return imagen_tk
    except Exception as e:
        print(f"Error al cargar imagen {nombre_archivo}: {e}")
        return None

# --- Funciones de Clima ---
def obtener_clima_async(ciudad, callback):
    """
    Obtiene la información del clima de forma asíncrona para no bloquear la UI.
    Utiliza wttr.in para obtener el clima.
    """
    def _get_clima():
        try:
            url = f"https://wttr.in/{ciudad}?format=%t+%C"
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                texto = resp.text.strip()
                partes = texto.split(" ", 1)
                temp = partes[0]
                desc = partes[1] if len(partes) > 1 else ""
                desc_esp = traducciones.get(desc, desc)
                callback(f"Clima: {temp} {desc_esp}")
            else:
                callback("Clima: No disponible")
        except requests.exceptions.RequestException:
            callback("Clima: Error de conexión")
        except Exception as e:
            print(f"Error inesperado al obtener clima: {e}")
            callback("Clima: No disponible")
    
    threading.Thread(target=_get_clima, daemon=True).start()

# --- Interfaz de Usuario ---
class AplicacionRelojMundial:
    def __init__(self, master):
        self.master = master
        master.title("Reloj Mundial Cultural")
        
        master.attributes('-fullscreen', True)
        master.bind("<Escape>", lambda e: master.attributes('-fullscreen', False))

        self.setup_styles()
        self.create_widgets()
        
        self.master.after(100, self.initial_setup_and_update) 
        
        self.cargar_progreso_al_inicio()
        
        self.sabias_update_interval_ms = 10000
        self.sabias_update_job = None
        
    def initial_setup_and_update(self):
        """Realiza la configuración inicial que requiere que la ventana ya esté renderizada."""
        self.master.update_idletasks() 
        
        self.update_city_specific_data()
        self.schedule_sabias_update()
        
        self.update_all()

    def setup_styles(self):
        """Configura los estilos de TTK para una apariencia moderna y transparente."""
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('TCombobox',
                        font=('Arial', 12),
                        padding=5,
                        fieldbackground=COLORES["texto_claro"],
                        background=COLORES["acento_principal"],
                        foreground=COLORES["texto_oscuro"])
        style.map('TCombobox',
                  fieldbackground=[('readonly', COLORES["texto_claro"])],
                  selectbackground=[('readonly', COLORES["acento_principal"])],
                  selectforeground=[('readonly', COLORES["texto_claro"])])

        style.configure("TProgressbar",
                        thickness=20,
                        background=COLORES["acento_principal"],
                        troughcolor=COLORES["borde"],
                        bordercolor=COLORES["fondo_principal"],
                        lightcolor=COLORES["acento_principal"],
                        darkcolor=COLORES["acento_principal"],
                        borderradius=10,
                        troughrelief='flat')

        style.configure("ProgressLabel.TLabel",
                        font=("Arial", 14, "bold"),
                        foreground=COLORES["texto_claro"],
                        background=COLORES["fondo_principal"])
        
        style.configure('Transparent.TLabel',
                        foreground=COLORES["texto_claro"],
                        font=("Indie Flower", 40, "bold"))

        style.configure('TransparentSmall.TLabel',
                        foreground=COLORES["texto_claro"],
                        font=("Indie Flower", 20))
        
        style.configure('Sabias.TLabel',
                        foreground=COLORES["texto_claro"],
                        font=("Arial", 14, "italic"),
                        wraplength=600)

        style.configure('Central.TFrame', background=COLORES["fondo_principal"])

        style.configure('Toplevel.TLabel',
                        background=COLORES["fondo_secundario"],
                        foreground=COLORES["texto_claro"])
        style.configure('Toplevel.TFrame',
                        background=COLORES["fondo_secundario"])
        # Nuevo estilo para el botón de Siguiente Trivia
        style.configure('TriviaNav.TButton',
                        font=('Arial Rounded MT Bold', 12),
                        foreground=COLORES["texto_claro"],
                        background=COLORES["acento_principal"],
                        relief="flat",
                        padding=10)
        style.map('TriviaNav.TButton',
                  background=[('active', COLORES["acento_secundario"])])


    def wrap_text_on_canvas(self, text, canvas_width_percentage, font_name, font_size, font_style="normal"):
        """
        Envuelve (wrap) el texto manualmente para un elemento de texto de Tkinter Canvas.
        Calcula los saltos de línea basados en el ancho del canvas y las métricas de la fuente.
        El parámetro font_style ahora mapea correctamente a slant o weight.
        """
        if not text:
            return ""

        canvas_width = self.main_canvas.winfo_width()
        if canvas_width < 100: 
            return text 
        
        max_width_pixels = int(canvas_width * canvas_width_percentage)

        try:
            if font_style == "italic":
                canvas_font = font.Font(family=font_name, size=font_size, slant=font.ITALIC)
            elif font_style == "bold":
                canvas_font = font.Font(family=font_name, size=font_size, weight=font.BOLD)
            elif font_style == "bold italic":
                canvas_font = font.Font(family=font_name, size=font_size, weight=font.BOLD, slant=font.ITALIC)
            else:
                canvas_font = font.Font(family=font_name, size=font_size)
        except tk.TclError:
            if font_style == "italic":
                canvas_font = font.Font(family="Arial", size=font_size, slant=font.ITALIC)
            elif font_style == "bold":
                canvas_font = font.Font(family="Arial", size=font_size, weight=font.BOLD)
            elif font_style == "bold italic":
                canvas_font = font.Font(family="Arial", size=font_size, weight=font.BOLD, slant=font.ITALIC)
            else:
                canvas_font = font.Font(family="Arial", size=font_size)


        words = text.split(' ')
        wrapped_lines = []
        current_line = []
        current_line_width = 0

        for word in words:
            word_width = canvas_font.measure(word + " ")
            
            if current_line_width + word_width <= max_width_pixels:
                current_line.append(word)
                current_line_width += word_width
            else:
                if current_line:
                    wrapped_lines.append(" ".join(current_line))
                current_line = [word]
                current_line_width = canvas_font.measure(word + " ")
        
        if current_line:
            wrapped_lines.append(" ".join(current_line))
            
        return "\n".join(wrapped_lines)
    
    def on_city_selected(self, event=None):
        """Se ejecuta cuando se selecciona una nueva ciudad en el combobox."""
        self.update_city_specific_data()
        self.update_progress_display()
        self.update_all(resize_only=False)

    def create_widgets(self):
        """Crea todos los widgets (elementos de interfaz) de la aplicación."""
        self.main_canvas = tk.Canvas(self.master, bg=COLORES["fondo_principal"], highlightthickness=0)
        self.main_canvas.place(x=0, y=0, relwidth=1, relheight=1)

        self.fondo_img_id = self.main_canvas.create_image(0, 0, anchor=tk.CENTER)
        
        self.hora_id_canvas = self.main_canvas.create_text(
            0, 0, font=("Indie Flower", 50, "bold"), fill=COLORES["texto_claro"], anchor=tk.CENTER
        )
        self.fecha_id_canvas = self.main_canvas.create_text(
            0, 0, font=("Indie Flower", 25), fill=COLORES["texto_claro"], anchor=tk.CENTER
        )
        self.clima_id_canvas = self.main_canvas.create_text(
            0, 0, font=("Indie Flower", 22), fill=COLORES["texto_claro"], anchor=tk.CENTER
        )
        self.sabias_id_canvas = self.main_canvas.create_text(
            0, 0,
            fill=COLORES["texto_claro"],
            anchor=tk.CENTER,
            font=font.Font(family="Arial", size=14, slant=font.ITALIC)
        )

        self.ciudad_var = tk.StringVar(value="Buenos Aires")
        self.selector = ttk.Combobox(self.main_canvas, textvariable=self.ciudad_var,
                                     values=list(CIUDADES.keys()), state="readonly",
                                     font=('Arial', 12))
        self.selector_id = self.main_canvas.create_window(
            20, 10, window=self.selector, anchor=tk.NW
        )
        self.selector.bind("<<ComboboxSelected>>", self.on_city_selected)

        self.button_ids = []
        x_offset = 200
        y_offset = 10

        def on_enter(event, button):
            button.config(background=COLORES["acento_principal"], foreground=COLORES["texto_claro"])
        def on_leave(event, button):
            button.config(background=COLORES["fondo_principal"], foreground=COLORES["texto_claro"])

        def create_styled_button(text, command):
            btn = tk.Button(self.main_canvas,
                            text=text,
                            command=command,
                            font=('Arial Rounded MT Bold', 13),
                            fg=COLORES["texto_claro"],
                            bg=COLORES["fondo_principal"],
                            activebackground=COLORES["acento_secundario"],
                            activeforeground=COLORES["texto_claro"],
                            relief="flat",
                            bd=0,
                            highlightthickness=0,
                            padx=18, pady=12)
            btn.bind("<Enter>", lambda e, b=btn: on_enter(e, b))
            btn.bind("<Leave>", lambda e, b=btn: on_leave(e, b))
            return btn

        self.btn_curiosidades = create_styled_button("Curiosidades", self.mostrar_curiosidades)
        self.button_ids.append(self.main_canvas.create_window(
            x_offset, y_offset, window=self.btn_curiosidades, anchor=tk.NW
        ))
        self.main_canvas.update_idletasks()
        x_offset += self.btn_curiosidades.winfo_width() + 10

        self.btn_frases = create_styled_button("Frases Típicas", self.mostrar_frases)
        self.button_ids.append(self.main_canvas.create_window(
            x_offset, y_offset, window=self.btn_frases, anchor=tk.NW
        ))
        self.main_canvas.update_idletasks()
        x_offset += self.btn_frases.winfo_width() + 10

        self.btn_eventos = create_styled_button("Eventos Históricos", self.mostrar_eventos)
        self.button_ids.append(self.main_canvas.create_window(
            x_offset, y_offset, window=self.btn_eventos, anchor=tk.NW
        ))
        self.main_canvas.update_idletasks()
        x_offset += self.btn_eventos.winfo_width() + 10
        
        self.btn_trivia = create_styled_button("Jugar Trivia", self.lanzar_pregunta)
        self.button_ids.append(self.main_canvas.create_window(
            x_offset, y_offset, window=self.btn_trivia, anchor=tk.NW
        ))
        self.main_canvas.update_idletasks()

        self.progreso_frame = tk.Frame(self.main_canvas, bg=COLORES["fondo_principal"])
        self.progreso_frame_id = self.main_canvas.create_window(0, self.master.winfo_screenheight(), window=self.progreso_frame, anchor=tk.SW)

        self.progreso_label = ttk.Label(self.progreso_frame, text="", style="ProgressLabel.TLabel")
        self.progreso_label.pack(side="left", padx=20, pady=5)

        self.progreso_barra = ttk.Progressbar(self.progreso_frame, orient="horizontal", length=300, mode="determinate", maximum=100)
        self.progreso_barra.pack(side="right", padx=20, pady=5)

        self.main_canvas.bind("<Configure>", self.on_canvas_resize)

    def on_canvas_resize(self, event):
        """Se llama cuando el tamaño del canvas cambia (ej. por pantalla completa)."""
        self.update_all(resize_only=True)

    def cargar_progreso_al_inicio(self):
        """Carga el progreso de trivia al iniciar la aplicación y actualiza la barra."""
        cargar_progreso()
        self.update_progress_display()

    def update_city_specific_data(self):
        """Actualiza el clima y el dato 'Sabías qué?' cuando cambia la ciudad."""
        ciudad = self.ciudad_var.get()
        self.main_canvas.itemconfig(self.clima_id_canvas, text=self.wrap_text_on_canvas("Clima: Obteniendo...", 0.7, "Indie Flower", 22))
        obtener_clima_async(ciudad, lambda text: self.main_canvas.itemconfig(self.clima_id_canvas, text=self.wrap_text_on_canvas(text, 0.7, "Indie Flower", 22)))
        
        self.actualizar_sabias()

    def schedule_sabias_update(self):
        """Programa la actualización periódica del texto 'Sabías qué?'."""
        if self.sabias_update_job:
            self.master.after_cancel(self.sabias_update_job)

        self.actualizar_sabias()
        
        self.sabias_update_job = self.master.after(self.sabias_update_interval_ms, self.schedule_sabias_update)

    def update_all(self, resize_only=False):
        """
        Actualiza la hora, fecha y la imagen de fondo según la ciudad seleccionada.
        Se llama cada segundo para mantener la hora actualizada.
        'resize_only' es un flag para indicar si solo se debe reubicar los elementos y reajustar los wraps,
        sin pedir datos nuevos como el clima o los "Sabías qué?".
        """
        canvas_ancho = self.main_canvas.winfo_width()
        canvas_alto = self.main_canvas.winfo_height()

        if canvas_ancho == 0 or canvas_alto == 0:
            self.master.after(100, self.update_all, resize_only)
            return

        ciudad = self.ciudad_var.get()
        zona, fondo_img_nombre = CIUDADES.get(ciudad, (None, None))
        if fondo_img_nombre:
            fondo_tk_img = cargar_imagen(fondo_img_nombre, canvas_ancho, canvas_alto)
            if fondo_tk_img:
                self.main_canvas.itemconfig(self.fondo_img_id, image=fondo_tk_img)
                self.main_canvas.coords(self.fondo_img_id, canvas_ancho / 2, canvas_alto / 2)
                self.main_canvas.image = fondo_tk_img
                self.main_canvas.lower(self.fondo_img_id)

        zona_horaria = pytz.timezone(zona)
        ahora = datetime.now(zona_horaria)
        hora_str = ahora.strftime("%H:%M:%S")
        self.main_canvas.itemconfig(self.hora_id_canvas, text=hora_str)

        fecha_en = ahora.strftime("%A %d de %B de %Y")
        fecha_es = traducir_fecha(fecha_en)
        self.main_canvas.itemconfig(self.fecha_id_canvas, text=fecha_es)

        current_clima_text = self.main_canvas.itemcget(self.clima_id_canvas, "text")
        self.main_canvas.itemconfig(self.clima_id_canvas, text=self.wrap_text_on_canvas(current_clima_text, 0.7, "Indie Flower", 22))

        current_sabias_text = self.main_canvas.itemcget(self.sabias_id_canvas, "text")
        self.main_canvas.itemconfig(self.sabias_id_canvas, text=self.wrap_text_on_canvas(current_sabias_text, 0.8, "Arial", 14, "italic"))

        self.main_canvas.coords(self.hora_id_canvas, canvas_ancho / 2, canvas_alto * 0.30)
        self.main_canvas.coords(self.fecha_id_canvas, canvas_ancho / 2, canvas_alto * 0.45)
        self.main_canvas.coords(self.clima_id_canvas, canvas_ancho / 2, canvas_alto * 0.60)
        self.main_canvas.coords(self.sabias_id_canvas, canvas_ancho / 2, canvas_alto * 0.75)
        
        self.main_canvas.coords(self.selector_id, 20, 10)
        
        x_offset = 200
        y_offset = 10
        buttons_to_reposition = [self.btn_curiosidades, self.btn_frases, self.btn_eventos, self.btn_trivia]
        for i, btn in enumerate(buttons_to_reposition):
            self.main_canvas.coords(self.button_ids[i], x_offset, y_offset)
            self.main_canvas.update_idletasks() 
            x_offset += btn.winfo_width() + 10 

        self.main_canvas.coords(self.progreso_frame_id, 0, canvas_alto)

        self.master.after(1000, self.update_all, False)

    def actualizar_sabias(self):
        """Actualiza el label "¿Sabías qué?" con un dato aleatorio del país actual."""
        ciudad = self.ciudad_var.get()
        pais = PAISES.get(ciudad)
        curiosidades = datos_curiosos.get(pais)
        
        dato_original = ""
        if curiosidades:
            dato_original = random.choice(curiosidades)
            wrapped_dato = self.wrap_text_on_canvas(f"¿Sabías qué? {dato_original}", 0.8, "Arial", 14, "italic")
            self.main_canvas.itemconfig(self.sabias_id_canvas, text=wrapped_dato)
        else:
            wrapped_dato = self.wrap_text_on_canvas("No hay datos curiosos disponibles para este país.", 0.8, "Arial", 14, "italic")
            self.main_canvas.itemconfig(self.sabias_id_canvas, text=wrapped_dato)
        
        canvas_ancho = self.main_canvas.winfo_width()
        canvas_alto = self.main_canvas.winfo_height()
        
        self.main_canvas.coords(self.sabias_id_canvas, canvas_ancho / 2, canvas_alto * 0.75)

    def mostrar_lista(self, titulo, lista):
        """
        Crea una ventana Toplevel genérica para mostrar listas de datos (curiosidades, frases, eventos).
        Incluye una barra de desplazamiento si la lista es larga.
        """
        ciudad = self.ciudad_var.get()
        fondo_img_nombre = CIUDADES.get(ciudad, (None, None))[1]
        ancho = 500
        alto = 400
        fondo_tk_img = cargar_imagen(fondo_img_nombre, ancho, alto) if fondo_img_nombre else None

        ventana_cultural = tk.Toplevel(self.master)
        ventana_cultural.title(titulo)
        ventana_cultural.geometry(f"{ancho}x{alto}")
        ventana_cultural.transient(self.master)
        ventana_cultural.grab_set()
        ventana_cultural.configure(bg=COLORES["fondo_secundario"])

        # Fondo de imagen
        if fondo_tk_img:
            fondo_label = tk.Label(ventana_cultural, image=fondo_tk_img)
            fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
            ventana_cultural.fondo_img = fondo_tk_img  # Evita que la imagen sea recolectada por el GC

        frame_scroll = ttk.Frame(ventana_cultural, style='Toplevel.TFrame')
        frame_scroll.pack(padx=20, pady=20, fill="both", expand=True)

        canvas = tk.Canvas(frame_scroll, borderwidth=0, background=COLORES["fondo_secundario"], highlightthickness=0)
        vscroll = ttk.Scrollbar(frame_scroll, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vscroll.set)

        vscroll.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner_frame = ttk.Frame(canvas, style='Toplevel.TFrame')
        canvas.create_window((0, 0), window=inner_frame, anchor="nw", width=440)

        def _on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        inner_frame.bind("<Configure>", _on_frame_configure)

        if lista:
            for item in lista:
                label = ttk.Label(inner_frame, text=f"• {item}", font=("Arial", 12),
                                  wraplength=400, justify="left", style='Toplevel.Toplevel.TLabel')
                label.pack(padx=10, pady=5, fill="x")
        else:
            ttk.Label(inner_frame, text="No hay datos disponibles.", font=("Arial", 12, "italic"),
                      style='Toplevel.TLabel').pack(padx=10, pady=20)
        
        ventana_cultural.protocol("WM_DELETE_WINDOW", lambda: self.cerrar_ventana_cultural(ventana_cultural))
        self.master.wait_window(ventana_cultural)

    def cerrar_ventana_cultural(self, ventana):
        """Libera el grab y destruye la ventana modal."""
        ventana.grab_release()
        ventana.destroy()

    def mostrar_curiosidades(self):
        """Muestra la ventana con datos curiosos del país actual."""
        ciudad = self.ciudad_var.get()
        pais = PAISES.get(ciudad, "Desconocido")
        curiosidades = datos_curiosos.get(pais, [])
        self.mostrar_lista(f"Curiosidades de {pais}", curiosidades)

    def mostrar_frases(self):
        """Muestra la ventana con frases típicas del país actual."""
        ciudad = self.ciudad_var.get()
        pais = PAISES.get(ciudad, "Desconocido")
        frases = datos_frases.get(pais, [])
        self.mostrar_lista(f"Frases típicas de {pais}", frases)

    def mostrar_eventos(self):
        """Muestra la ventana con eventos históricos del país actual."""
        ciudad = self.ciudad_var.get()
        pais = PAISES.get(ciudad, "Desconocido")
        eventos = datos_eventos.get(pais, [])
        self.mostrar_lista(f"Eventos históricos de {pais}", eventos)

    def lanzar_pregunta(self):
        """
        Lanza una pregunta de trivia al usuario para el país seleccionado.
        Muestra opciones y verifica la respuesta.
        """
        ciudad = self.ciudad_var.get()
        pais = PAISES.get(ciudad, ciudad)
        lista_preguntas_pais = preguntas.get(pais, [])
        
        if not lista_preguntas_pais:
            messagebox.showinfo("Trivia", f"No hay preguntas de trivia disponibles para {pais} aún.")
            return

        # **Cambio 1: Dimensiones de la ventana de trivia**
        ancho_ventana = 800
        alto_ventana = 600

        ventana_q = tk.Toplevel(self.master)
        ventana_q.title("Pregunta Cultural")
        ventana_q.geometry(f"{ancho_ventana}x{alto_ventana}")
        ventana_q.configure(bg=COLORES["fondo_secundario"])
        ventana_q.transient(self.master)
        ventana_q.grab_set()

        fondo_img_nombre = CIUDADES.get(ciudad, (None, None))[1]
        fondo_tk_img = cargar_imagen(fondo_img_nombre, ancho_ventana, alto_ventana) 
        if fondo_tk_img:
            fondo_label = tk.Label(ventana_q, image=fondo_tk_img)
            fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
            ventana_q.fondo_img = fondo_tk_img

        def cerrar_ventana_q():
            ventana_q.grab_release()
            ventana_q.destroy()

        ventana_q.protocol("WM_DELETE_WINDOW", cerrar_ventana_q)

        frame_pregunta = ttk.Frame(ventana_q, style='Toplevel.TFrame', padding=(25, 20))
        frame_pregunta.pack(padx=30, pady=25, fill="both", expand=True)

        ttk.Label(frame_pregunta, text="Trivia Cultural", font=("Arial Rounded MT Bold", 20, "bold"),
                  foreground=COLORES["acento_principal"], background=COLORES["fondo_secundario"]).pack(pady=(10, 5))

        # **Cambio 1: Aumentar el wraplength de la pregunta para las nuevas dimensiones**
        pregunta_label = ttk.Label(frame_pregunta, text="",
                                    font=("Arial", 16, "bold"), # Fuente un poco más grande
                                    foreground=COLORES["texto_claro"],
                                    background=COLORES["fondo_secundario"], wraplength=700, # Ajustado para 800px de ancho
                                    justify="center")
        pregunta_label.pack(pady=(15, 25))

        resultado_label = ttk.Label(frame_pregunta, font=("Arial", 16, "bold"), background=COLORES["fondo_secundario"])
        resultado_label.pack(pady=(10, 0))

        botones_opciones = []
        colores_opciones = ["#8ab6d9", "#d6a2e8", "#ffd39b", "#a7e9af"]

        # Botón de "Siguiente Pregunta"
        btn_siguiente = ttk.Button(frame_pregunta, text="Siguiente Pregunta →",
                                   command=lambda: siguiente_pregunta(pais, lista_preguntas_pais),
                                   state="disabled", # Inicialmente deshabilitado
                                   style='TriviaNav.TButton')
        btn_siguiente.pack(pady=(20, 10))

        def responder(opcion_elegida, pregunta_idx):
            correcto = opcion_elegida == lista_preguntas_pais[pregunta_idx]["respuesta"]
            if correcto:
                resultado_label.config(text="✔ ¡Correcto!", foreground=COLORES["exito"])
                registrar_respuesta_correcta(pais, pregunta_idx)
                self.update_progress_display()
                # **Cambio 2: Avance automático si la respuesta es correcta**
                ventana_q.after(1500, lambda: siguiente_pregunta(pais, lista_preguntas_pais)) # Espera 1.5 segundos y avanza
            else:
                resultado_label.config(text=f"✘ Incorrecto\nRespuesta: {lista_preguntas_pais[pregunta_idx]['respuesta']}",
                                       foreground=COLORES["error"])
                btn_siguiente.config(state="normal") # Habilita el botón de siguiente solo si es incorrecto
            
            for btn in botones_opciones:
                btn.config(state="disabled") # Deshabilita los botones de opción después de responder

        def mostrar_pregunta(pregunta_idx_a_mostrar):
            pregunta_actual_data = lista_preguntas_pais[pregunta_idx_a_mostrar]
            pregunta_label.config(text=pregunta_actual_data["pregunta"])
            resultado_label.config(text="") # Limpiar el resultado anterior

            for btn in botones_opciones:
                btn.destroy() # Eliminar botones anteriores si existen
            botones_opciones.clear() # Limpiar la lista

            for i, opcion in enumerate(pregunta_actual_data["opciones"]):
                btn = tk.Button(
                    frame_pregunta,
                    text=opcion,
                    font=("Arial", 14, "bold"), # Fuente un poco más grande
                    bg=colores_opciones[i % len(colores_opciones)],
                    fg=COLORES["texto_oscuro"],
                    activebackground=COLORES["acento_principal"],
                    activeforeground=COLORES["texto_claro"],
                    relief="raised",
                    bd=2,
                    cursor="hand2",
                    command=lambda o=opcion, idx=pregunta_idx_a_mostrar: responder(o, idx)
                )
                btn.pack(fill="x", padx=60, pady=10) # Mayor padx y pady para botones
                botones_opciones.append(btn)
            
            btn_siguiente.config(state="disabled") # El botón "Siguiente" siempre deshabilitado al mostrar nueva pregunta

        def siguiente_pregunta(current_pais, todas_las_preguntas):
            pendientes = [i for i in range(len(todas_las_preguntas)) if i not in progreso.get(current_pais, {}).get("preguntas_correctas", [])]
            
            if not pendientes:
                messagebox.showinfo("Trivia", f"¡Ya completaste todas las preguntas de {current_pais}! ¡Felicidades!")
                cerrar_ventana_q() 
                return
            
            # Obtener una nueva pregunta aleatoria de las pendientes
            siguiente_idx = random.choice(pendientes)
            mostrar_pregunta(siguiente_idx)

        # Mostrar la primera pregunta al lanzar la ventana
        pendientes_inicio = [i for i in range(len(lista_preguntas_pais)) if i not in progreso.get(pais, {}).get("preguntas_correctas", [])]
        if not pendientes_inicio: 
            messagebox.showinfo("Trivia", f"¡Ya completaste todas las preguntas de {pais}! ¡Felicidades!")
            cerrar_ventana_q()
            return
        
        idx_inicial = random.choice(pendientes_inicio)
        mostrar_pregunta(idx_inicial)
        
        self.master.wait_window(ventana_q)


    def update_progress_display(self):
        """Actualiza el texto y el valor de la barra de progreso de trivia."""
        ciudad_actual = self.ciudad_var.get()
        pais_actual = PAISES.get(ciudad_actual, ciudad_actual)
        
        porcentaje_local = calcular_porcentaje(pais_actual)
        porcentaje_global = calcular_progreso_global()

        self.progreso_label.config(text=f"Progreso en {pais_actual}: {porcentaje_local}% | Global: {porcentaje_global}%")
        self.progreso_barra['value'] = porcentaje_local

    def draw_text_with_outline(self, canvas, x, y, text, font, fill, outline="black", outline_width=2, anchor="center"):
        # Dibuja el texto varias veces alrededor para simular el borde
        for dx in range(-outline_width, outline_width+1):
            for dy in range(-outline_width, outline_width+1):
                if dx != 0 or dy != 0:
                    canvas.create_text(x+dx, y+dy, text=text, font=font, fill=outline, anchor=anchor)
        # Dibuja el texto principal encima
        canvas.create_text(x, y, text=text, font=font, fill=fill, anchor=anchor)

# --- Ejecución de la Aplicación ---
if __name__ == "__main__":
    if not os.path.exists(RUTA_IMAGENES):
        os.makedirs(RUTA_IMAGENES)
        print(f"Directorio '{RUTA_IMAGENES}' creado. Por favor, coloca las imágenes de fondo aquí.")
    
    root = tk.Tk()
    app = AplicacionRelojMundial(root)
    root.mainloop()
