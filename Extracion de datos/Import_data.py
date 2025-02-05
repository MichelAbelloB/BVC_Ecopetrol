import os
import pyodbc
import pandas as pd

# Directorio donde se encuentra el archivo
directorio = r'C:\Users\Michel Abello\Downloads'  # Cambia esto según tu ubicación

# Buscar el archivo que comienza con 'ECOPETROL'
archivo = None
for archivo_encontrado in os.listdir(directorio):
    if archivo_encontrado.startswith('ECOPETROL') and archivo_encontrado.endswith('.csv'):
        archivo = archivo_encontrado
        break  # Sale del bucle cuando encuentra el primer archivo que cumpla la condición

# Verificar si se encontró el archivo
if archivo is None:
    print("No se encontró un archivo CSV que comience con 'ECOPETROL'.")
else:
    # Leer el archivo CSV
    df = pd.read_csv(os.path.join(directorio, archivo), sep=';')  # Asumimos que el separador es ';'

    # Verificar si la columna 'Fecha' está en un formato adecuado
    df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')  # Intentar convertir 'Fecha' a formato datetime

    # Asegurarse de que las columnas numéricas sean realmente numéricas
    numeric_columns = ['Precio cierre', 'Precio máximo', 'Precio promedio ponderado', 
                       'Precio mínimo', 'Variación absoluta', 'Variación porcentual', 
                       'Cantidad', 'Volumen']

    for col in numeric_columns:
        # Reemplazar comas por puntos y convertir a tipo numérico
        df[col] = df[col].replace({',': ''}, regex=True)  # Reemplazar coma por punto si es necesario
        df[col] = pd.to_numeric(df[col], errors='coerce')  # Convertir a numérico, reemplazando errores por NaN
        
        # Reemplazar valores nulos por 0 o algún valor predeterminado si es necesario
        df[col] = df[col].fillna(0)  # Reemplaza los NaN por 0 (o puedes usar otro valor como None)

        # Redondear los valores numéricos a 2 decimales si es necesario
        df[col] = df[col].round(2)

    # Conectar a SQL Server (autenticación de Windows)
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                          'SERVER=DESKTOP-JJKU9AB;'
                          'DATABASE=Investment;'
                          'Trusted_Connection=yes;')

    # Crear un cursor para ejecutar las consultas
    cursor = conn.cursor()

    # Insertar los datos en la tabla de SQL Server
    for index, row in df.iterrows():
        cursor.execute(''' 
            INSERT INTO Tabla_base (Fecha, Nemotecnico, Precio_cierre, Precio_maximo, Precio_promedio_ponderado,
            Precio_minimo, Variacion_absoluta, Variacion_porcentual, Cantidad, Volumen)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            row['Fecha'], row['Nemotécnico'], row['Precio cierre'], row['Precio máximo'], 
            row['Precio promedio ponderado'], row['Precio mínimo'], row['Variación absoluta'],
            row['Variación porcentual'], row['Cantidad'], row['Volumen'])

    # Confirmar la transacción
    conn.commit()

    # Cerrar la conexión
    cursor.close()
    conn.close()

    print("Datos importados exitosamente.")





