# Reloj Mundial 

Este proyecto es una aplicación de escritorio interactiva desarrollada con `tkinter` en Python. Combina la funcionalidad de un reloj mundial con información cultural y una divertida trivia sobre diferentes ciudades y países.

## Características

* **Reloj Mundial**: Muestra la hora y fecha actual de varias ciudades importantes alrededor del mundo.
* **Información Cultural**: Descubre datos curiosos, frases típicas y eventos históricos de cada país asociado a la ciudad seleccionada.
* **Trivia Interactiva**: Pon a prueba tus conocimientos con preguntas de trivia. El progreso se guarda localmente y te permite continuar donde lo dejaste.
* **Diseño Moderno**: Interfaz de usuario intuitiva y visualmente atractiva con estilos `ttk` y fondos de imagen dinámicos.

## Vista Previa

<!-- Reemplaza la siguiente línea con el Markdown de tu captura de pantalla -->
![Captura de Pantalla de la Aplicación Reloj Mundial](assets/foto.jpg)

## Cómo Ejecutar la Aplicación

Para ejecutar esta aplicación, necesitarás tener Python instalado en tu sistema. Se recomienda encarecidamente el uso de un entorno virtual para gestionar las dependencias del proyecto.

### 1. Configuración del Entorno

1.  **Clona o descarga el repositorio:**
    ```bash
    git clone https://github.com/BrunoEPaez/Relojmundial.git](https://github.com/BrunoEPaez/Relojmundial.git)
    cd tu-repositorio
    ```

2.  **Navega a la carpeta principal de tu proyecto:**
    ```bash
    cd C:\Users\...
    ```

3.  **Crea un entorno virtual:**
    ```bash
    python -m venv venv
    ```
    Si `python` no funciona, prueba con `py -m venv venv`.

4.  **Activa el entorno virtual:**
    * **Windows (PowerShell):**
        ```powershell
        .\venv\Scripts\Activate
        ```
    * **Windows (CMD):**
        ```cmd
        .\venv\Scripts\activate.bat
        ```
    * **macOS / Linux:**
        ```bash
        source venv/bin/activate
        ```
    Verás que el prompt de tu terminal cambia para indicar que el entorno virtual está activo (ej: `(venv) C:\...`).

### 2. Instalación de Dependencias

Con el entorno virtual activado, instala las librerías necesarias:

```bash
pip install Pillow requests pytz

    Pillow: Para el manejo y redimensionamiento de imágenes de fondo.

    requests: Para obtener datos de clima desde una API externa.

    pytz: Para la gestión de zonas horarias de las ciudades.

3. Estructura de Archivos y Carpetas

Asegúrate de que la estructura de tu proyecto sea la siguiente:

tu_proyecto/
├── imagenes/
│   ├── buenos_aires.jpg
│   ├── nueva_york.jpg
│   └── ... (Todas las imágenes de fondo para las ciudades)
├── venv/           (Carpeta del entorno virtual, creada en el paso 1)
├── .gitignore      (¡Muy importante! Archivo para ignorar archivos temporales y generados)
├── __init__.py     (Archivo vacío para que Python reconozca la carpeta como un paquete)
├── main_app.py     (Archivo principal de la aplicación)
├── config_data.py  (Contiene constantes, datos de ciudades, preguntas de trivia, etc.)
├── trivia_logic.py (Gestiona la lógica y persistencia de la trivia)
├── utils.py        (Funciones de utilidad: carga de imágenes, clima, traducción de fechas)
├── ui_components.py(Definiciones de estilos y componentes UI reutilizables)
└── progreso.json   (Archivo JSON para guardar el progreso de la trivia. Se creará/modificará automáticamente.)
