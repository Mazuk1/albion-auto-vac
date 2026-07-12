#!/usr/bin/env bash
# Registra o Albion_CriarOrdensVAC_linux.py como serviço de usuário do systemd,
# iniciado automaticamente ao fazer login na sessão gráfica.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"
SERVICE_NAME="albion-auto-vac.service"
SERVICE_DIR="$HOME/.config/systemd/user"
SERVICE_PATH="$SERVICE_DIR/$SERVICE_NAME"

if [ ! -d "$VENV_DIR" ]; then
    echo "Criando ambiente virtual em $VENV_DIR ..."
    python3 -m venv "$VENV_DIR"
fi

echo "Instalando dependências ..."
"$VENV_DIR/bin/pip" install -q --upgrade pip
"$VENV_DIR/bin/pip" install -q -r "$SCRIPT_DIR/requirements-linux.txt"

mkdir -p "$SERVICE_DIR"

cat > "$SERVICE_PATH" <<EOF
[Unit]
Description=Albion Online - Auto Criador de Ordens de Venda (VAC)
After=graphical-session.target
PartOf=graphical-session.target

[Service]
Type=simple
ExecStart=$VENV_DIR/bin/python3 $SCRIPT_DIR/Albion_CriarOrdensVAC_linux.py
Restart=on-failure
RestartSec=3

[Install]
WantedBy=graphical-session.target
EOF

systemctl --user daemon-reload
systemctl --user enable --now "$SERVICE_NAME"

echo
echo "Serviço instalado e iniciado: $SERVICE_NAME"
echo "Status:  systemctl --user status $SERVICE_NAME"
echo "Logs:    journalctl --user -u $SERVICE_NAME -f"
echo "Remover: systemctl --user disable --now $SERVICE_NAME && rm \"$SERVICE_PATH\""
