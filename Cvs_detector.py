import os
import shutil
import PyPDF2
import re
import sqlite3
from datetime import datetime


ruta_base = r"C:\Users\HP\Documents\CV proyect"

carpeta_cvs = os.path.join(ruta_base, "CVs")  
carpeta_validos = os.path.join(ruta_base, "CVs_validos")
carpeta_no_validos = os.path.join(ruta_base, "CVs_no_validos")  

os.makedirs(carpeta_cvs, exist_ok=True)
os.makedirs(carpeta_validos, exist_ok=True)
os.makedirs(carpeta_no_validos, exist_ok=True)


palabras_clave = ["python", "machine learning", "data analysis", "sql", "pandas"]


def extraer_texto_pdf(ruta_pdf):
    try:
        with open(ruta_pdf, "rb") as f:
            lector = PyPDF2.PdfReader(f)
            texto = ""
            for pagina in lector.pages:
                texto += pagina.extract_text() or ""
            return texto.lower()
    except:
        return ""


def limpiar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r'[^a-záéíóúüñ0-9\s]', '', texto)
    texto = re.sub(r'\s+', ' ', texto)
    return texto.strip()


conn = sqlite3.connect("cvs.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS cvs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_archivo TEXT,
    valido TEXT,
    palabras_encontradas TEXT,
    fecha_registro TEXT
)
""")
conn.commit()


for archivo in os.listdir(carpeta_cvs):
    if archivo.endswith(".pdf"):
        ruta_archivo = os.path.join(carpeta_cvs, archivo)

       
        texto = extraer_texto_pdf(ruta_archivo)
        texto_limpio = limpiar_texto(texto)

        
        encontradas = [palabra for palabra in palabras_clave if palabra in texto_limpio]

        if encontradas:
            shutil.copy(ruta_archivo, os.path.join(carpeta_validos, archivo))
            valido = "Sí"
        else:
            shutil.copy(ruta_archivo, os.path.join(carpeta_no_validos, archivo))
            valido = "No"

       
        cursor.execute("""
        INSERT INTO cvs (nombre_archivo, valido, palabras_encontradas, fecha_registro)
        VALUES (?, ?, ?, ?)
        """, (archivo, valido, ", ".join(encontradas) if encontradas else "N/A", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        conn.commit()

        print(f"Guardado en DB → {archivo} | Válido: {valido} | Palabras: {', '.join(encontradas) if encontradas else 'N/A'}")


conn.close()
print("✅ Proceso completado.")
