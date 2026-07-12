import time
import threading

from pynput import keyboard, mouse

# ============================================================
# CONFIGURAÇÕES — edite esta seção para ajustar ao seu setup
# ============================================================

# Tecla de atalho para ativar (segure para executar)
TECLA = keyboard.Key.f12

# Intervalo entre cada clique, em segundos (padrão: 0.1)
INTERVALO = 0.1

# Posições dos cliques na tela (x, y)
# Use o script calibrar_posicoes_linux.py para descobrir as coordenadas certas
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
print("  AUTO CLICKER — Albion Online (Linux)")
print("  Criador de Ordens de Venda (VAC)")
print("=" * 43)
print("  Atalho : Segure F12 para executar")
print("  Sair   : CTRL + C no terminal")
print("=" * 43)
print()

mouse_ctrl = mouse.Controller()
_teclas_pressionadas = set()
_lock = threading.Lock()


def _on_press(key):
    with _lock:
        _teclas_pressionadas.add(key)


def _on_release(key):
    with _lock:
        _teclas_pressionadas.discard(key)


def atalho_ativo():
    with _lock:
        return TECLA in _teclas_pressionadas


def clicar_loop():
    while atalho_ativo():
        for x, y in POSICOES:
            mouse_ctrl.position = (x, y)
            mouse_ctrl.click(mouse.Button.left)
            time.sleep(INTERVALO)


listener = keyboard.Listener(on_press=_on_press, on_release=_on_release)
listener.start()

try:
    while True:
        if atalho_ativo():
            clicar_loop()
        time.sleep(0.01)
except KeyboardInterrupt:
    print("\nAuto clicker encerrado.")
finally:
    listener.stop()
