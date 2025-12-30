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

def esperar_evento(imagens, timeout=30):
    inicio = time.time()
    while time.time() - inicio < timeout:
        for nome, img in imagens.items():
            pos = pyautogui.locateCenterOnScreen(img, confidence=0.9, grayscale=True)
            if pos:
                return nome, pos
        time.sleep(1)
    return None, None

def tratar_atualizacao(parceiro):
    evento, pos = esperar_evento({
        "confirmar": "confirmar.png",
        "erro": "erro.png"
    })

    if evento == "confirmar":
        pyautogui.click(pos)
        time.sleep(2)
        return "ok"

    elif evento == "erro":
        pyautogui.click(pos)
        time.sleep(1)

        fechar = esperar_evento({"fechar": "fechar.png"})[1]
        if fechar:
            pyautogui.click(fechar)
            time.sleep(1)

        # 🧾 LOG DO ERRO
        with open("erros.log", "a", encoding="utf-8") as f:
            f.write(f"[{time.strftime('%d/%m %H:%M:%S')}] Erro no parceiro {parceiro}\n")
        
        return "erro"

    else:
        with open("erros.log", "a", encoding="utf-8") as f:
            f.write(f"[{time.strftime('%d/%m %H:%M:%S')}] TIMEOUT parceiro {parceiro}\n")

        return "timeout"

def atualizar():
    parceiro = carregar_progresso()
    print(f"Iniciando do parceiro {parceiro}")

    while parceiro < TOTAL_PARCEIROS:
        print(f"🟢 Processando parceiro {parceiro}/{TOTAL_PARCEIROS}")

        clicar(1230, 110, 10)  # menu
        clicar(1230, 370, 10)  # atualizar receita
        resultado = tratar_atualizacao(parceiro)

        if resultado == "timeout":
            print("⚠️ Timeout detectado, interrompendo execução.")
            return
        
        elif resultado == "erro":
            print(f"⚠️ Erro no parceiro {parceiro}, seguindo para o próximo.")
        
        clicar(1230, 110, 10)  # menu
        clicar(1230, 345, 10)  # atualizar sefaz
        resultado = tratar_atualizacao(parceiro)

        if resultado == "timeout":
            print("⚠️ Timeout detectado, interrompendo execução.")
            return
        
        elif resultado == "erro":
            print(f"⚠️ Erro no parceiro {parceiro}, seguindo para o próximo.")  
        
        parceiro += 1
        salvar_progresso(parceiro)

        print(f"✔ Parceiro {parceiro} concluído")

        if parceiro % 3 == 0:
            time.sleep(60)

if __name__ == "__main__":
    atualizar()