#!/usr/bin/env python3
import subprocess
import sys
import os
import logging
from pathlib import Path

# Configuração de Log
LOG_FILE = "/var/log/auto_updater.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def is_root():
    return os.geteuid() == 0

def detect_distro():
    """Detecta a distribuição Linux baseada nos arquivos do sistema."""
    os_release = Path("/etc/os-release")
    if os_release.exists():
        content = os_release.read_text().lower()
        if "kali" in content:
            return "kali"
        elif "ubuntu" in content or "debian" in content or "mint" in content:
            return "debian_base"
        elif "fedora" in content or "rhel" in content or "centos" in content:
            return "fedora_base"
        elif "arch" in content:
            return "arch_base"
    return "unknown"

def run_command(command):
    try:
        env = os.environ.copy()
        env["DEBIAN_FRONTEND"] = "noninteractive"
        
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def update_system():
    distro = detect_distro()
    logging.info(f"Distribuição detectada: {distro.upper()}")

    if distro in ["kali", "debian_base"]:
        logging.info("Iniciando atualização (APT)...")
        run_command("apt-get update -y")
        success, out = run_command("apt-get dist-upgrade -y -o Dpkg::Options::='--force-confold'")
        if success:
            run_command("apt-get autoremove -y")
            run_command("apt-get autoclean")
            logging.info("Sistema atualizado com sucesso!")
        else:
            logging.error(f"Erro na atualização: {out}")

    elif distro == "fedora_base":
        logging.info("Iniciando atualização (DNF)...")
        success, out = run_command("dnf upgrade -y")
        if success:
            run_command("dnf autoremove -y")
            logging.info("Sistema atualizado com sucesso!")
        else:
            logging.error(f"Erro na atualização: {out}")

    elif distro == "arch_base":
        logging.info("Iniciando atualização (PACMAN)...")
        success, out = run_command("pacman -Syu --noconfirm")
        if success:
            logging.info("Sistema atualizado com sucesso!")
        else:
            logging.error(f"Erro na atualização: {out}")
            
    else:
        logging.critical("Distribuição não suportada por este script automatizado.")

if __name__ == "__main__":
    if not is_root():
        print("[-] Erro: Este script precisa ser executado como ROOT (sudo).", file=sys.stderr)
        sys.exit(1)
        
    try:
        update_system()
    except Exception as e:
        logging.critical(f"Erro inesperado no updater: {str(e)}")
