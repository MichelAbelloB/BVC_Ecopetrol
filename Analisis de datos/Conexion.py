import pyodbc
import pandas as pd
from win10toast import ToastNotifier

def consultar_sql_server():
    try:
        # Especifica los detalles de conexión
        server = r'DESKTOP-JJKU9AB'
        database = 'Investment'
        table = 'Tabla_base'
        driver = '{ODBC Driver 17 for SQL Server}'

        # Establece la conexión utilizando Windows Authentication
        conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;')

        # Mostrar notificación de proceso terminado
        toaster = ToastNotifier()
        toaster.show_toast("Conexión exitosa a SQL Server utilizando Windows Authentication", duration=10)

        # Ejecutar consulta SQL y obtener datos en un DataFrame de Pandas
        query = f'SELECT * FROM {table}'
        data = pd.read_sql(query, conn)

        # Cerrar la conexión
        conn.close()

        return data

    except pyodbc.Error as ex:
        print("Error al conectar a SQL Server:", ex)
        return None