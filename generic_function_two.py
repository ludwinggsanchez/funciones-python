
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from flask import send_file, jsonify
import os

def generic_function_two():
    # Cargar los dataframes
    df_departamentos = pd.read_csv("https://www.datos.gov.co/resource/ya3g-4kqg.csv")
    try:
        df_hurtos = pd.read_csv("datos_hurtos.csv")
    except FileNotFoundError:
        return jsonify({"error": "Archivo 'datos_hurtos.csv' no encontrado. Descárgalo y guárdalo aquí."}), 400

    # Cruzar datos
    df = df_hurtos.merge(df_departamentos, how="inner", left_on="COD_DEPTO", right_on="iddepto")

    # Convertir fecha con manejo de errores
    try:
        df['FECHA HECHO'] = pd.to_datetime(df['FECHA HECHO'], format='%Y-%m-%d', errors='coerce')
        if df['FECHA HECHO'].isnull().any():
            print("Advertencia: Algunas fechas no pudieron convertirse y se establecieron como NaT.")
        df['AÑO'] = df['FECHA HECHO'].dt.year
    except Exception as e:
        print(f"Error al convertir las fechas: {e}")
        df['AÑO'] = np.nan

    # Gráfico de caja (no se muestra en entorno no interactivo)
    # plt.figure(figsize=(15, 6))
    # sns.boxplot(y="CANTIDAD", data=df)
    # plt.title("Distribución de la variable cantidad de hurtos a personas")
    # plt.ylabel("Cantidad")
    # plt.show()

    # Gráfico por año (eliminando filas con año nulo)
    df_boxplot = df.dropna(subset=["AÑO"])
    if df_boxplot.empty:
        print("No hay datos válidos para graficar por año (todas las fechas son inválidas o faltantes).")
    else:
        # plt.figure(figsize=(15, 6))
        # sns.boxplot(x="AÑO", y="CANTIDAD", data=df_boxplot)
        # plt.title("Distribución por año")
        # plt.xlabel("Año")
        # plt.ylabel("Cantidad")
        # plt.show()
        pass

    print("Análisis completado.")

    # Crear un archivo CSV temporal con los datos procesados
    output_csv = 'Hurtos_en_colombia.csv'
    columnas_a_mostrar = ['COD_DEPTO','DEPARTAMENTO','MUNICIPIO','FECHA HECHO','AÑO','CANTIDAD']
    columnas_existentes = [col for col in columnas_a_mostrar if col in df.columns]
    df[columnas_existentes].to_csv(output_csv, index=False, encoding='utf-8-sig')

    print(f"Archivo guardado como {output_csv}")
    # Enviar el archivo como respuesta
    return send_file(output_csv, as_attachment=True)