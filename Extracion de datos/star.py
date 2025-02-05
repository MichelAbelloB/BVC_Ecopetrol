import pyautogui  
import time  
import pygetwindow as gw  
import webbrowser  
import datetime 
import subprocess
from win10toast import ToastNotifier

# URL del archivo en SharePoint
url = "https://www.bvc.com.co/renta-variable-mercado-local/ECOPETROL?tab=informacion-del-emisor"

# Abrir el enlace en el navegador predeterminado
webbrowser.open(url)

home = None
intentos = 0

# Bucle para verificar si el home de la página es visible
while home is None:
    time.sleep(5)
    intentos += 1
    try:
        # Obtener la ventana con el título "Bolsa de Valores"
        ventana = pyautogui.getWindowsWithTitle("Bolsa de Valores")[0]
        if ventana.isActive:
            home = ventana
        elif intentos == 5:
            ventana.minimize()
            ventana.maximize()
            print("Estoy dentro de los 5 intentos para ver el home de la web")
            intentos = 0
    except IndexError:
        pass  # Si no encuentra la ventana, continúa intentando

while home is None:
    time.sleep(5)
    intentos += 1
    try:
        # Obtener la ventana con el título "Bolsa de Valores"
        ventana = pyautogui.getWindowsWithTitle("Bolsa de Valores")[0]
        if ventana.isActive:
            home = ventana
        elif intentos == 5:
            ventana.minimize()
            ventana.maximize()
            print("Estoy dentro de los 5 intentos para ver el home de la web")
            intentos = 0
    except IndexError:
        pass  # Si no encuentra la ventana, continúa intentando

pyautogui.moveTo(950, 550)

time.sleep(10)
pyautogui.click()

# Desplazarse hacia abajo en la página
time.sleep(10)
pyautogui.scroll(-2000)  

# Obtener la fecha actual
hoy = datetime.datetime.now()
dia_actual = hoy.day

pyautogui.moveTo(750, 500)  
pyautogui.click()

time.sleep(1) 

base_x = 850  
base_y = 750  
cell_width = 30  
cell_height = 30  

# Calcular fila y columna del día actual (suponiendo que el calendario empieza el lunes y día 1 siempre está en la primera fila)

columna = (dia_actual - 1) % 7
fila = (dia_actual - 1) // 7
pyautogui.moveTo(base_x + columna * cell_width, base_y + fila * cell_height)
pyautogui.doubleClick()

pyautogui.moveTo(1300, 500)
pyautogui.click()

toast = ToastNotifier()

# Mostrar una notificación
toast.show_toast("Descarga completada", "El documento ha sido descargado exitosamente.", duration=10)
subprocess.call(["python", "Import_data.py"])

