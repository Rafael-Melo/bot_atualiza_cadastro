import pyautogui
import time
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGENS = os.path.join(BASE_DIR, "..", "src", "bot_atualiza_cadastro", "imagens")

img = os.path.join(IMAGENS, "confirmar.png")

print("Caminho da imagem:", img)
print("Existe?", os.path.exists(img))

time.sleep(3)
print(pyautogui.locateCenterOnScreen(img, confidence=0.7))
