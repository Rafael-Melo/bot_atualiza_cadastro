import pyautogui
import time
import json

pyautogui.FAILSAFE = True

TOTAL_PARCEIROS = 16584
ARQUIVO_PROG = "progresso.json"

def carregar_progresso():
    try:
        with open(ARQUIVO_PROG, "r") as f:
            return json.load(f)["parceiro"]
    except:
        return 0
    
def salvar_progresso(valor):
    with open(ARQUIVO_PROG, "w") as f:
        json.dump({"parceiro": valor}, f)

def clicar(x, y, espera=2):
    pyautogui.click(x, y, duration=1)
    time.sleep(espera)

def esperar_imagem(img, timeout=30):
    inicio = time.time()
    while time.time() - inicio < timeout:
        pos = pyautogui.locateCenterOnScreen(img, confidence=0.8)
        if pos:
            return pos
        time.sleep(1)
    return None   

def atualizar():
    parceiro = carregar_progresso()
    print(f"Iniciando do parceiro {parceiro}")

    while parceiro < TOTAL_PARCEIROS:
        print(f"🟢 Processando parceiro {parceiro}/{TOTAL_PARCEIROS}")

        clicar(100, 200, 10)  # menu
        clicar(200, 300, 10)  # atualizar receita
        botao = esperar_imagem("confirmar.png")
        if botao:
            pyautogui.click(botao)
        else:
            print("❌ Botão não encontrado")
            return
        clicar(100, 200, 10)  # menu
        clicar(200, 350, 10)  # atualizar sefaz
        botao = esperar_imagem("confirmar.png")
        if botao:
            pyautogui.click(botao)
        else:
            print("❌ Botão não encontrado")
            return
        clicar(600, 700, 10)  # salvar
        clicar(700, 700, 10)  # próximo

        parceiro += 1
        salvar_progresso(parceiro)

        print(f"✔ Parceiro {parceiro} concluído")

        if parceiro % 3 == 0:
            time.sleep(60)

if __name__ == "__main__":
    atualizar()