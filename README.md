# Albion Online — Auto Criador de Ordens de Venda

Automatiza a criação de pedidos de venda no mercado do **Albion Online**. Enquanto você estiver com a aba **Vender → Criar Pedido de Venda** aberta, o script realiza todos os cliques necessários para registrar o item pelo **preço atual − 1 prata**, um após o outro, apenas segurando um atalho de teclado.

---

## O que ele faz

Ao segurar **ALT + 0**, o script executa em loop a seguinte sequência de cliques:

| # | Ação no jogo |
|---|---|
| 1 | Clica no campo de preço (já com valor − 1 prata) |
| 2 | Confirma a quantidade |
| 3 | Clica em **Criar Pedido de Venda** |

O processo se repete enquanto a tecla for mantida pressionada, avançando automaticamente para o próximo item do inventário.

---

## Pré-requisitos

- Windows 10/11 **ou** Linux (Ubuntu e derivados)
- Python 3.8 ou superior (veja o guia abaixo)
- Albion Online instalado

> **Linux:** os pacotes `pyautogui` e `keyboard` usados no Windows não funcionam no Linux sem privilégios de root. Use os arquivos `Albion_CriarOrdensVAC_linux.py`, `calibrar_posicoes_linux.py` e `requirements-linux.txt`, descritos na seção [Uso no Linux](#uso-no-linux-ubuntu) — eles usam `pynput`, que funciona sem root via X11/XWayland.

---

## Instalando o Python no Windows

> Pule esta etapa se o Python já estiver instalado.

**1.** Acesse [python.org/downloads](https://www.python.org/downloads/) e clique em **Download Python 3.x.x** (a versão mais recente).

**2.** Execute o instalador baixado. Na primeira tela, marque obrigatoriamente a opção:

```
☑ Add Python to PATH
```

> Sem essa opção marcada, os comandos `python` e `pip` não vão funcionar no terminal.

**3.** Clique em **Install Now** e aguarde a instalação terminar.

**4.** Verifique se foi instalado corretamente abrindo o **Prompt de Comando** (`Win + R` → digite `cmd` → Enter) e executando:

```
python --version
```

A resposta deve ser algo como `Python 3.12.x`. Se aparecer um erro, reinicie o computador e tente novamente.

---

## Instalação

**1.** Baixe o projeto — clique em **Code → Download ZIP** no GitHub e extraia a pasta, ou clone via terminal:

```bash
git clone https://github.com/Mazuk1/albion-auto-vac.git
cd albion-auto-vac
```

**2.** Instale as dependências do projeto abrindo o terminal **dentro da pasta** e executando:

```bash
pip install -r requirements.txt
```

Aguarde o download terminar. Você verá algo como:

```
Successfully installed pyautogui-0.9.54 keyboard-0.13.5 ...
```

Se aparecer o erro `'pip' não é reconhecido`, feche e reabra o terminal e tente novamente. Se persistir, reinstale o Python marcando a opção **Add Python to PATH**.

---

## Configuração

> **Importante:** as posições dos cliques dependem da sua resolução de monitor. O script vem calibrado para uma tela específica — siga os passos abaixo para ajustar ao seu setup.

### Passo 1 — Descobrir suas coordenadas

Execute o calibrador e posicione o cursor sobre cada elemento no jogo, pressionando **ESPAÇO** para capturar:

```bash
python calibrar_posicoes.py
```

Capture as 3 posições na seguinte ordem (com o jogo aberto na tela de Criar Pedido de Venda):

1. Campo de preço (com o valor − 1 prata já preenchido)
2. Campo de quantidade / confirmação
3. Botão **Criar Pedido de Venda**

O script vai exibir o bloco pronto para copiar:

```
POSICOES = [
    (1234, 567),   # 1. descrição do clique
    (890, 1011),   # 2. descrição do clique
    (1213, 1415),  # 3. descrição do clique
]
```

### Passo 2 — Aplicar as coordenadas

Abra `Albion_CriarOrdensVAC.py` e substitua o bloco `POSICOES` pelo resultado do calibrador.

### Outras configurações disponíveis

No topo do arquivo `Albion_CriarOrdensVAC.py`:

```python
# Tecla de atalho (padrão: ALT + 0)
TECLA_1 = 'alt'
TECLA_2 = '0'

# Intervalo entre cliques em segundos (padrão: 0.1)
INTERVALO = 0.1
```

Você pode trocar `'0'` por qualquer tecla (`'1'`, `'f1'`, `'insert'`, etc.) e ajustar o intervalo conforme a velocidade da sua conexão.

---

## Como usar

1. Abra o Albion Online e vá ao mercado
2. Selecione a aba **Vender** e marque a opção **Criar Pedido de Venda**
3. Execute o script:

```bash
python Albion_CriarOrdensVAC.py
```

4. No jogo, clique no primeiro item do inventário para abrir o painel de venda
5. Segure **ALT + 0** — o script vai criar o pedido e repetir para o próximo item automaticamente
6. Solte a tecla quando quiser pausar
7. Para encerrar o script, pressione **CTRL + C** no terminal

---

## Iniciando automaticamente com o Windows

O repositório inclui um script PowerShell para registrar a tarefa no **Agendador de Tarefas** do Windows, executando o auto clicker assim que você fizer login:

```powershell
$python = (python -c "import sys; print(sys.executable)")
$script = "$PWD\Albion_CriarOrdensVAC.py"

Register-ScheduledTask `
  -TaskName "AlbionCriarOrdensVAC" `
  -Trigger (New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME) `
  -Action (New-ScheduledTaskAction -Execute $python -Argument "`"$script`"") `
  -Settings (New-ScheduledTaskSettingsSet -ExecutionTimeLimit (New-TimeSpan -Hours 0) -MultipleInstances IgnoreNew) `
  -RunLevel Limited -Force
```

Para remover a tarefa depois:

```powershell
Unregister-ScheduledTask -TaskName "AlbionCriarOrdensVAC" -Confirm:$false
```

---

## Uso no Linux (Ubuntu)

Os pacotes `pyautogui` e `keyboard` da versão Windows não são compatíveis com o Linux: `keyboard` exige privilégios de root para ler eventos de teclado, e `pyautogui` depende de bibliotecas X11 que não vêm instaladas por padrão. Por isso o repositório inclui uma versão alternativa baseada em `pynput`, que funciona no Ubuntu (X11 ou Wayland com XWayland) sem precisar de root:

- `Albion_CriarOrdensVAC_linux.py` — versão Linux do auto clicker
- `calibrar_posicoes_linux.py` — versão Linux do calibrador de posições
- `requirements-linux.txt` — dependências (`pynput`)

### Instalação manual

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-linux.txt
.venv/bin/python3 calibrar_posicoes_linux.py   # para calibrar as posições
.venv/bin/python3 Albion_CriarOrdensVAC_linux.py
```

Depois de calibrar, cole o resultado no bloco `POSICOES` de `Albion_CriarOrdensVAC_linux.py`, da mesma forma descrita na seção [Configuração](#configuração).

### Iniciando automaticamente com o Ubuntu

O script `instalar_autostart_linux.sh` cria um ambiente virtual, instala as dependências e registra um serviço de usuário do `systemd` que inicia o auto clicker automaticamente ao fazer login na sessão gráfica:

```bash
./instalar_autostart_linux.sh
```

Comandos úteis depois de instalado:

```bash
systemctl --user status albion-auto-vac.service      # ver status
journalctl --user -u albion-auto-vac.service -f      # ver logs em tempo real
systemctl --user disable --now albion-auto-vac.service && rm ~/.config/systemd/user/albion-auto-vac.service   # remover
```

---

## Perguntas frequentes

**Os cliques estão na posição errada — o que faço?**
Use o `calibrar_posicoes.py` para capturar as coordenadas corretas para a sua resolução e cole o resultado no arquivo principal.

**O script clica muito rápido / lento.**
Aumente ou diminua o valor de `INTERVALO` (em segundos) no topo do `Albion_CriarOrdensVAC.py`.

**Quero usar outra tecla de atalho.**
Troque os valores de `TECLA_1` e `TECLA_2`. Referência de nomes de teclas: [documentação do keyboard](https://github.com/boppreh/keyboard#api).

**O script para de funcionar depois de um tempo.**
Verifique se o Albion não mudou o layout da tela de venda após uma atualização. Recalibre as posições com `calibrar_posicoes.py`.

---

## Aviso

Este projeto é apenas para fins de automação pessoal e aprendizado. Use com responsabilidade e de acordo com os termos de serviço do Albion Online.

---

## Licença

[MIT](LICENSE)
