#!/usr/bin/env bash
set -euo pipefail
echo "=== CRUCIBLE-VM INSTALLER ==="
if [ "$EUID" -ne 0 ]; then
    echo "[ERROR] Ejecuta como root: sudo ./install_client.sh"
    exit 1
fi
if [ ! -e /dev/kvm ]; then
    echo "[ERROR] /dev/kvm no disponible."
    exit 1
fi
chmod 666 /dev/kvm
apt-get update -qq && apt-get install -y -qq curl jq iptables python3 python3-venv python3-pip bridge-utils iproute2 > /dev/null

FIRECRACKER_VERSION="v1.7.0"
ARCH="$(uname -m)"
if ! command -v firecracker &> /dev/null; then
    TMP_DIR=$(mktemp -d)
    curl -sSL "https://github.com/firecracker-microvm/firecracker/releases/download/${FIRECRACKER_VERSION}/firecracker-${FIRECRACKER_VERSION}-${ARCH}.tgz" -o "${TMP_DIR}/firecracker.tgz"
    tar -xzf "${TMP_DIR}/firecracker.tgz" -C "${TMP_DIR}"
    install -m 755 "${TMP_DIR}/release-${FIRECRACKER_VERSION}-${ARCH}/firecracker-${FIRECRACKER_VERSION}-${ARCH}" /usr/local/bin/firecracker
    install -m 755 "${TMP_DIR}/release-${FIRECRACKER_VERSION}-${ARCH}/jailer-${FIRECRACKER_VERSION}-${ARCH}" /usr/local/bin/jailer
    rm -rf "${TMP_DIR}"
fi

TMPFS_DIR="/mnt/crucible-tmpfs"
mkdir -p "${TMPFS_DIR}"
if ! mountpoint -q "${TMPFS_DIR}"; then
    mount -t tmpfs -o size=2G,mode=0777 tmpfs "${TMPFS_DIR}"
    grep -qs "${TMPFS_DIR}" /etc/fstab || echo "tmpfs ${TMPFS_DIR} tmpfs size=2G,mode=0777 0 0" >> /etc/fstab
fi

INSTALL_DIR="/opt/crucible"
mkdir -p "${INSTALL_DIR}"
[ -f "$(pwd)/main.py" ] && cp -r "$(pwd)"/* "${INSTALL_DIR}/"

python3 -m venv "${INSTALL_DIR}/venv"
"${INSTALL_DIR}/venv/bin/pip" install --upgrade pip -q
[ -f "${INSTALL_DIR}/requirements.txt" ] && "${INSTALL_DIR}/venv/bin/pip" install -r "${INSTALL_DIR}/requirements.txt" -q || "${INSTALL_DIR}/venv/bin/pip" install fastapi uvicorn pydantic requests -q

cat << SYSTEMD_EOF > /etc/systemd/system/crucible.service
[Unit]
Description=Crucible-VM Isolation Engine
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=${INSTALL_DIR}
Environment="TMPFS_DIR=${TMPFS_DIR}"
ExecStart=${INSTALL_DIR}/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=3
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
SYSTEMD_EOF

systemctl daemon-reload
systemctl enable crucible.service -q
systemctl restart crucible.service
echo "[✓] Crucible-VM desplegado y activo en http://127.0.0.1:8000"
