from flask import jsonify

def function_two():
    return jsonify({'message': 'This is function two.'})
import pandas as pd
ruta_archivo = "/content/sample_data/Registros-de-ventas.xlsx"
print(df)
df = pd.DataFrame(data)
df["Tipo de producto"] = df["Tipo de producto"].astype(str)
df["Fecha pedido"] = pd.to_datetime(df["Fecha pedido"])
df["Importe venta total"] = df["Importe venta total"].astype(float)
data = {
    'Tipo de producto': [],
    'Fecha pedido': [],
    'Importe venta total': []
data = {
    'Tipo de producto': [],
    'Fecha pedido': [],
    'Importe venta total': []
}
df = pd.DataFrame(data)
df["Tipo de producto"] = df["Tipo de producto"].astype(str)
df["Fecha pedido"] = pd.to_datetime(df["Fecha pedido"])
df["Importe venta total"] = df["Importe venta total"].astype(float)
df["Fecha pedido"] = pd.to_datetime(df["Fecha pedido"])
df['Año'] = df["Fecha pedido"].dt.year
promedio = df.groupby(['Tipo de producto', 'Año'])['Importe venta total'].mean().reset_index()

print(resultado)
