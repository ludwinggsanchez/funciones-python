from flask import jsonify, request
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def generic_function_two():
    # Configurar credenciales para Google Sheets
    scope = ["https://spreadsheets.google.com/feeds ", "https://www.googleapis.com/auth/drive "]
    credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    gc = gspread.authorize(credentials)

    # Abrir el Google Sheet por URL
    spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1IJVH31MqUVSxv3mVnhtST9bwvUFLUqBNxmaEZ9DNEPg/edit?usp=sharing'
    spreadsheet = gc.open_by_url(spreadsheet_url)
    worksheet = spreadsheet.sheet1
    data = worksheet.get_all_records()
    df_hurtos = pd.DataFrame(data)

    # Cargar los datos de departamentos
    df_departamentos = pd.read_csv(" https://www.datos.gov.co/resource/ya3g-4kqg.csv ")

    # Cruzar datos
    df = df_hurtos.merge(df_departamentos, how="inner", left_on="COD_DEPTO", right_on="iddepto")

    # Convertir fecha
    df['FECHA HECHO'] = pd.to_datetime(df['FECHA HECHO'], format='%d/%m/%Y')
    df['AÑO'] = df['FECHA HECHO'].dt.year

    # Gráfico de caja
    plt.figure(figsize=(15, 6))
    sns.boxplot(y="CANTIDAD", data=df)
    plt.title("Distribución de la variable cantidad de hurtos a personas")
    plt.ylabel("Cantidad")
    plt.show()

    # Gráfico por año
    plt.figure(figsize=(15, 6))
    sns.boxplot(x="AÑO", y="CANTIDAD", data=df)
    plt.title("Distribución por año")
    plt.xlabel("Año")
    plt.ylabel("Cantidad")
    plt.show()

    print("Análisis completado.")

    return jsonify({'message': 'This is a scaffold for generic_function_two.'})