"""
Ferramenta de calibração de posições para o Albion_CriarOrdensVAC.py

Como usar:
  1. Execute este script: python calibrar_posicoes.py
  2. Posicione o cursor do mouse sobre o elemento desejado na tela
  3. Pressione ESPAÇO para capturar a posição atual
  4. Repita para cada posição necessária
  5. Pressione ESC para encerrar e ver o resultado final
"""

import keyboard
import time

try:
    import pyautogui
except ImportError:
    print("Erro: pyautogui não instalado. Execute: pip install pyautogui")
    exit(1)

posicoes_capturadas = []

print("=" * 50)
print("  CALIBRADOR DE POSIÇÕES — Albion Auto Clicker")
print("=" * 50)
print("  ESPAÇO  → capturar posição atual do cursor")
print("  ESC     → encerrar e mostrar resultado")
print("=" * 50)
print()

while True:
    if keyboard.is_pressed('space'):
        x, y = pyautogui.position()
        posicoes_capturadas.append((x, y))
        print(f"  [{len(posicoes_capturadas)}] Capturado: ({x}, {y})")
        time.sleep(0.3)  # debounce

    if keyboard.is_pressed('esc'):
        break

    time.sleep(0.01)

print()
print("=" * 50)
print("  Resultado — cole em Albion_CriarOrdensVAC.py:")
print("=" * 50)
print()
print("POSICOES = [")
for i, (x, y) in enumerate(posicoes_capturadas, 1):
    print(f"    ({x}, {y}),   # {i}. descrição do clique")
print("]")
print()
