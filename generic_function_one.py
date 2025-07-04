from flask import jsonify, request

def generic_function_one():
    # TODO: Implement your logic here
    return jsonify({'message': 'This is a scaffold for generic_function_one.'})
# Script profesional para encontrar la localidad con mayor tasa de mortalidad

import csv


import os

# Buscar el archivo CSV en el directorio actual y superiores
def encontrar_csv(nombre_archivo):
    ruta = os.path.abspath(os.path.dirname(__file__))
    while True:
        posible = os.path.join(ruta, nombre_archivo)
        if os.path.isfile(posible):
            return posible
        padre = os.path.dirname(ruta)
        if padre == ruta:
            break
        ruta = padre
    return None

csv_path = encontrar_csv("osb_mortalidad_dnt.csv")
if not csv_path:
    raise FileNotFoundError("No se encontró el archivo osb_mortalidad_dnt.csv en este directorio ni en los superiores.")


max_tasa = -1
localidad_max = None
anio_max = None


# Abrir el archivo con manejo de errores de codificación
import codecs
try:
    with codecs.open(csv_path, encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f, delimiter=';')
        # Detectar la columna de año aunque tenga caracteres extraños
        anio_col = None
        for col in reader.fieldnames:
            if col and col.lower().replace('ñ', 'n').replace('ã', 'a').replace('�', 'n').startswith('a') and 'o' in col.lower():
                anio_col = col
                break
        for i, row in enumerate(reader, 1):
            if not row:
                print(f"[DEBUG] Fila vacía en línea {i+1}")
                continue
            localidad = row.get('Localidad') or row.get('localidad')
            tasa_str = (row.get('Tasa') or row.get('tasa') or '').replace(',', '.')
            anio = row.get(anio_col) if anio_col and row.get(anio_col) else 'N/A'
            if not localidad or not tasa_str:
                print(f"[DEBUG] Faltan datos en línea {i+1}: {row}")
                continue
            try:
                tasa = float(tasa_str)
            except (ValueError, TypeError):
                print(f"[DEBUG] Tasa inválida en línea {i+1}: '{tasa_str}'")
                continue
            if tasa > max_tasa and localidad and localidad.lower() != 'distrito':
                max_tasa = tasa
                localidad_max = localidad
                anio_max = anio
except Exception as e:
    print(f"[ERROR] No se pudo leer el archivo CSV correctamente: {e}")


if localidad_max:
    print(f"La localidad con mayor tasa de mortalidad es: {localidad_max} (Año: {anio_max}, Tasa: {max_tasa})")
else:
    print("No se encontraron datos válidos de localidades.")