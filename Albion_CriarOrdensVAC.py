import pyautogui
import keyboard
import time

# ============================================================
# CONFIGURAÇÕES — edite esta seção para ajustar ao seu setup
# ============================================================

# Teclas de atalho para ativar (segure para executar)
TECLA_1 = 'alt'
TECLA_2 = '0'

# Intervalo entre cada clique, em segundos (padrão: 0.1)
INTERVALO = 0.1

# Posições dos cliques na tela (x, y)
# Use o script calibrar_posicoes.py para descobrir as coordenadas certas
# para a sua resolução de monitor.
#
# Fluxo esperado no jogo (aba Vender > Criar Pedido de Venda):
#   1. Clique no campo de preço e ajusta para preço atual -1 prata
#   2. Clique em confirmar/aceitar o preço
#   3. Clique em "Criar Pedido de Venda"
POSICOES = [
    (2509, 864),   # 1. Campo/confirmação de preço (-1 prata)
    (1665, 1260),  # 2. Confirmar quantidade
    (2298, 1464),  # 3. Botão "Criar Pedido de Venda"
]

# ============================================================

print("=" * 43)
print("  AUTO CLICKER — Albion Online")
print("  Criador de Ordens de Venda (VAC)")
print("=" * 43)
print(f"  Atalho : Segure {TECLA_1.upper()} + {TECLA_2.upper()} para executar")
print(f"  Sair   : CTRL + C no terminal")
print("=" * 43)
print()


def clicar_loop():
    while keyboard.is_pressed(TECLA_1) and keyboard.is_pressed(TECLA_2):
        for x, y in POSICOES:
            pyautogui.click(x, y)
            time.sleep(INTERVALO)


try:
    while True:
        if keyboard.is_pressed(TECLA_1) and keyboard.is_pressed(TECLA_2):
            clicar_loop()
        time.sleep(0.01)
except KeyboardInterrupt:
    print("\nAuto clicker encerrado.")
