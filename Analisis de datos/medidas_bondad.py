from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from io import BytesIO
import base64
import numpy as np
import seaborn as sns
from Conexion import consultar_sql_server


data = consultar_sql_server()

df = pd.DataFrame(data)

# Función lambda para convertir valores de string a float
def convert_to_float(x):
    try:
        return float(str(x).replace(',', ''))
    except ValueError:
        return np.nan

# Aplicar la conversión a cada columna relevante
df['Precio_cierre'] = df['Precio_cierre'].apply(convert_to_float)
df['Precio_maximo'] = df['Precio_maximo'].apply(convert_to_float)
df['Precio_promedio_ponderado'] = df['Precio_promedio_ponderado'].apply(convert_to_float)
df['Precio_minimo'] = df['Precio_minimo'].apply(convert_to_float)
df['Variacion_absoluta'] = df['Variacion_absoluta'].apply(convert_to_float)
df['Variacion_porcentual'] = df['Variacion_porcentual'].apply(convert_to_float)
df['Cantidad'] = df['Cantidad'].apply(convert_to_float)
df['Volumen'] = df['Volumen'].apply(convert_to_float)

# Eliminar filas con valores faltantes (si es necesario)
df.dropna(inplace=True)

# Variables independientes (features)
X = df[['Precio_maximo', 'Precio_promedio_ponderado', 'Precio_minimo', 'Variacion_absoluta', 'Variacion_porcentual', 'Cantidad', 'Volumen']]

# Variable dependiente (target)
y = df['Precio_cierre']

# Crear un modelo de ejemplo (en la práctica, usarías un modelo entrenado)
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X, y)

# Predicciones
y_pred = model.predict(X)

# Cálculo de las métricas
r2 = r2_score(y, y_pred)
mae = mean_absolute_error(y, y_pred)
mse = mean_squared_error(y, y_pred)
rmse = np.sqrt(mse)
mape = np.mean(np.abs((y - y_pred) / y)) * 100

print(f'R²: {r2}')
print(f'MAE: {mae}')
print(f'MSE: {mse}')
print(f'RMSE: {rmse}')
print(f'MAPE: {mape}')