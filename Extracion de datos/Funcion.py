import pyautogui 
import time 

def pressingKey(key,times = 1):
    for i in range(times):
        # Presiona la tecla key varias veces con un intervalo de 0.6 segundos.
        time.sleep(0.6)
        pyautogui.press(key)     
# Funcion de Minimizar todas las ventanas para mostrar el escritorio.

def make_window_visible(target_window):
    time.sleep(1)
    count = 0
    encontrado = None
    print("Cantidad de ventanas activas: ",len(pyautogui.getAllWindows()))
    
    while encontrado is None:
        window_title = pyautogui.getActiveWindowTitle()
        if target_window not in window_title:
            count += 1
            with pyautogui.hold('alt'):
                pyautogui.press('tab')
                for _ in range(0, count):                    
                    pyautogui.press('left')
        else:
            print("La ventana " + target_window + " es ahora visible y esta activa!")
            encontrado = window_title
        time.sleep(0.25)
