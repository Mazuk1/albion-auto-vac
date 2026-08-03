import time
import threading

from pynput import keyboard, mouse

# ============================================================
# CONFIGURAÇÕES — edite esta seção para ajustar ao seu setup
# ============================================================

# Teclas de atalho para ativar (segure para executar)
TECLA_1 = {keyboard.Key.alt_l, keyboard.Key.alt_r}
TECLA_2 = keyboard.KeyCode.from_char('0')

# Intervalo entre cada clique, em segundos (padrão: 0.1)
INTERVALO = 0.1

# Escala do display no KDE (Configurações > Telas). No Wayland, o KWin
# interpreta o movimento do cursor em coordenadas lógicas, mas a calibração
# devolve pixels físicos — por isso dividimos pela escala ao clicar.
# Use 1.0 se estiver em sessão X11 ou sem escala.
ESCALA = 1.7

# Posições dos cliques na tela (x, y)
# Use o script calibrar_posicoes_linux.py para descobrir as coordenadas certas
# para a sua resolução de monitor.
#
# Fluxo esperado no jogo (aba Vender > Criar Pedido de Venda):
#   1. Clique no campo de preço e ajusta para preço atual -1 prata
#   2. Clique em confirmar/aceitar o preço
#   3. Clique em "Criar Pedido de Venda"
POSICOES = [
    (2474, 873),   # 1. Campo/confirmação de preço (-1 prata)
    (1658, 1259),  # 2. Confirmar quantidade
    (2301, 1458),  # 3. Botão "Criar Pedido de Venda"
]

# ============================================================

print("=" * 43)
print("  AUTO CLICKER — Albion Online (Linux)")
print("  Criador de Ordens de Venda (VAC)")
print("=" * 43)
print("  Atalho : Segure ALT + 0 para executar")
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
        return bool(_teclas_pressionadas & TECLA_1) and TECLA_2 in _teclas_pressionadas


def clicar_loop():
    while atalho_ativo():
        for x, y in POSICOES:
            mouse_ctrl.position = (x / ESCALA, y / ESCALA)
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
