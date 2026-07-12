"""
Ferramenta de calibração de posições para o Albion_CriarOrdensVAC_linux.py

Como usar:
  1. Execute este script: python calibrar_posicoes_linux.py
  2. Posicione o cursor do mouse sobre o elemento desejado na tela
  3. Pressione ESPAÇO para capturar a posição atual
  4. Repita para cada posição necessária
  5. Pressione ESC para encerrar e ver o resultado final
"""

import threading
import time

from pynput import keyboard, mouse

mouse_ctrl = mouse.Controller()
posicoes_capturadas = []
_teclas_pressionadas = set()
_lock = threading.Lock()
_encerrar = threading.Event()


def _on_press(key):
    with _lock:
        ja_pressionada = key in _teclas_pressionadas
        _teclas_pressionadas.add(key)

    if ja_pressionada:
        return

    if key == keyboard.Key.space:
        x, y = mouse_ctrl.position
        posicoes_capturadas.append((x, y))
        print(f"  [{len(posicoes_capturadas)}] Capturado: ({x}, {y})")
    elif key == keyboard.Key.esc:
        _encerrar.set()


def _on_release(key):
    with _lock:
        _teclas_pressionadas.discard(key)


print("=" * 50)
print("  CALIBRADOR DE POSIÇÕES — Albion Auto Clicker")
print("=" * 50)
print("  ESPAÇO  → capturar posição atual do cursor")
print("  ESC     → encerrar e mostrar resultado")
print("=" * 50)
print()

listener = keyboard.Listener(on_press=_on_press, on_release=_on_release)
listener.start()

try:
    while not _encerrar.is_set():
        time.sleep(0.01)
finally:
    listener.stop()

print()
print("=" * 50)
print("  Resultado — cole em Albion_CriarOrdensVAC_linux.py:")
print("=" * 50)
print()
print("POSICOES = [")
for i, (x, y) in enumerate(posicoes_capturadas, 1):
    print(f"    ({x}, {y}),   # {i}. descrição do clique")
print("]")
print()
