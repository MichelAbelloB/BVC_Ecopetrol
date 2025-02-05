from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.dates as mdates
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest
import mplfinance as mpf
from prophet import Prophet
from io import BytesIO
import base64
import seaborn as sns
import numpy as np
from datetime import datetime, timedelta
from Conexion import consultar_sql_server

app = Flask(__name__)

def make_arima_prediction(data, column, steps=30):
    """
    Realiza predicción ARIMA para una serie temporal
    """
    try:
        model = ARIMA(data[column], order=(1,1,1))  # Parámetros simplificados
        results = model.fit()
        forecast = results.forecast(steps=steps)
        return forecast
    except Exception as e:
        print(f"Error en predicción ARIMA para {column}: {str(e)}")
        return None

@app.route('/')
def home():
    try:
        # Cargar los datos
        data = consultar_sql_server()
        
        if data is None or data.empty:
            return "Error: No se pudieron obtener datos de la base de datos."
        
        # Imprimir información de debug
        print("\nColumnas disponibles en el DataFrame:")
        for col in data.columns:
            print(f"- '{col}'")
        
        # Convertir columnas numéricas
        numeric_columns = [
            'Precio_cierre',
            'Precio_maximo',
            'Precio_promedio_ponderado',
            'Precio_minimo',
            'Variacion_absoluta',
            'Variacion_porcentual',
            'Cantidad',
            'Volumen'
        ]
        
        # Convertir columnas a float
        for column in numeric_columns:
            data[column] = data[column].apply(lambda x: float(str(x).replace(',', '').replace('.', '.')))

        # Convertir la columna Fecha
        data['Fecha'] = pd.to_datetime(data['Fecha'])
        data = data.sort_values('Fecha')

        # 1. Gráfico de distribución (plot_url)
        plt.figure(figsize=(12, 8))
        sns.histplot(data['Precio_cierre'], kde=True)
        plt.title('Distribución de Precio de Cierre')
        plt.xlabel('Precio de Cierre')
        plt.ylabel('Frecuencia')
        
        img = BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')
        plt.close()
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

        # 2. Matriz de correlación (plot_url_corr)
        plt.figure(figsize=(12, 8), facecolor='#28443c')
        correlation_matrix = data[numeric_columns].corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
        plt.xticks(color='white')
        plt.yticks(color='white')
        plt.title('Matriz de Correlación', color='white')
        
        img_corr = BytesIO()
        plt.savefig(img_corr, format='png', bbox_inches='tight')
        plt.close()
        img_corr.seek(0)
        plot_url_corr = base64.b64encode(img_corr.getvalue()).decode()

        # 3. Histogramas múltiples (plot_url_hist)
        fig, axes = plt.subplots(len(numeric_columns), 1, figsize=(12, 4*len(numeric_columns)))
        for i, column in enumerate(numeric_columns):
            sns.histplot(data[column], ax=axes[i], kde=True)
            axes[i].set_title(f'Distribución de {column}')
        plt.tight_layout()
        
        img_hist = BytesIO()
        plt.savefig(img_hist, format='png', bbox_inches='tight')
        plt.close()
        img_hist.seek(0)
        plot_url_hist = base64.b64encode(img_hist.getvalue()).decode()

        # 4. Regresión lineal (plot_url_reg_lineal)
        data['Fecha_num'] = (data['Fecha'] - data['Fecha'].min()).dt.days
        X = data['Fecha_num'].values.reshape(-1, 1)
        y = data['Precio_cierre'].values
        model = LinearRegression()
        model.fit(X, y)
        data['Prediccion'] = model.predict(X)

        plt.figure(figsize=(12, 8), facecolor='#28443c')
        plt.plot(data['Fecha'], data['Precio_cierre'], label='Datos reales')
        plt.plot(data['Fecha'], data['Prediccion'], label='Regresión lineal')
        plt.title('Análisis de Tendencia con Regresión Lineal',  color='white')
        plt.xlabel('Fecha', color='white')
        plt.ylabel('Precio de Cierre', color='white')
        plt.legend()
        plt.xticks(rotation=45, color='white')
        plt.yticks(color='white')
        
        img_reg = BytesIO()
        plt.savefig(img_reg, format='png', bbox_inches='tight')
        plt.close()
        img_reg.seek(0)
        plot_url_reg_lineal = base64.b64encode(img_reg.getvalue()).decode()

        # 5. Gráfico de anomalías (plot_url_anomalies)
        plt.figure(figsize=(12, 8))
        plt.plot(data['Fecha'], data['Variacion_absoluta'], label='Variación Absoluta')
        plt.plot(data['Fecha'], data['Variacion_porcentual'], label='Variación Porcentual')
        plt.title('Variaciones de Precio')
        plt.xlabel('Fecha')
        plt.ylabel('Variación')
        plt.legend()
        plt.xticks(rotation=45)
        
        img_anom = BytesIO()
        plt.savefig(img_anom, format='png', bbox_inches='tight')
        plt.close()
        img_anom.seek(0)
        plot_url_anomalies = base64.b64encode(img_anom.getvalue()).decode()

        # 6. Gráfico de predicción del precio de cierre (plot_url_candlestick)
        plt.figure(figsize=(5, 4), facecolor='#28443c')
        plt.rcParams.update({'font.size': 6})  # Establecer tamaño de fuente global
        
        # Fechas futuras para la predicción
        future_dates = pd.date_range(start=data['Fecha'].iloc[-1], periods=31)[1:]
        
        # Hacer predicción solo para precio de cierre
        forecast_cierre = make_arima_prediction(data, 'Precio_cierre')
        
        # Graficar datos históricos y predicción
        plt.plot(data['Fecha'], data['Precio_cierre'], 
                label='Precio de Cierre Histórico', 
                color='blue', 
                linewidth=1)
        
        if forecast_cierre is not None:
            plt.plot(future_dates, forecast_cierre, 
                    label='Predicción', 
                    color='red', 
                    linestyle='--', 
                    linewidth=1)
        
        plt.title('Proyección precio de cierre', 
                 pad=10,
                 fontsize=6,
                 color='white')
        plt.xlabel('Fecha', fontsize=6, color='white')
        plt.ylabel('Precio', fontsize=6, color='white')
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # Ajustar la leyenda con texto más pequeño
        plt.legend(loc='upper right', fontsize=6, frameon=True)
        
        # Formato para los ejes con texto más pequeño
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45, fontsize=4, color='white')
        plt.yticks(fontsize=4, color='white')
        
        # Reducir el número de fechas mostradas en el eje x
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        
        # Ajustar los márgenes
        plt.tight_layout()
        
        # Guardar el gráfico
        img_candle = BytesIO()
        plt.savefig(img_candle, format='png', bbox_inches='tight', dpi=300)
        plt.close()
        img_candle.seek(0)
        plot_url_candlestick = base64.b64encode(img_candle.getvalue()).decode()

        # Renderizar template con todos los gráficos
        return render_template('index.html',
                             plot_url=plot_url,
                             plot_url_corr=plot_url_corr,
                             plot_url_hist=plot_url_hist,
                             plot_url_reg_lineal=plot_url_reg_lineal,
                             plot_url_anomalies=plot_url_anomalies,
                             plot_url_candlestick=plot_url_candlestick)

    except Exception as e:
        import traceback
        print("\nError detallado:")
        traceback.print_exc()
        return f"Error en el procesamiento: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)