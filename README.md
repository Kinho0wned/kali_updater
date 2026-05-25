# Auto-Linux-Updater 🐧🔄

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Linux-orange.svg)](https://www.kernel.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Uma ferramenta de automação robusta desenvolvida em Python e integrada ao **Systemd** para gerenciar, verificar e aplicar atualizações de segurança e repositórios de forma totalmente automática no Linux. Compatível nativamente com **Kali Linux**, distribuições baseadas em **Debian/Ubuntu**, **Fedora** e **Arch Linux**.

---

## 🎯 Motivação e Objetivo

Manter sistemas Linux (especialmente distribuições de Rolling Release como o Kali Linux ou Arch) atualizados é crucial para a segurança cibernética e estabilidade das ferramentas. No entanto, executar manualmente os comandos de atualização diariamente pode ser ineficiente.

O **Auto-Linux-Updater** resolve isso operando em segundo plano de forma não intrusiva. Ele detecta a distribuição hospedeira, escolhe o gerenciador de pacotes correto e agenda rotinas de manutenção sem que o usuário precise abrir o terminal.

---

## 🛠️ Como Funciona (Arquitetura)

O projeto é dividido em duas camadas principais:

1. **A Lógica (Script Python):** Responsável por ler os arquivos de release do sistema (`/etc/os-release`), identificar o ecossistema (APT, DNF ou Pacman), tratar as variáveis de ambiente para evitar travas interativas e registrar cada ação em um arquivo de log centralizado.
2. **A Automação (Systemd):** Utiliza um par de arquivos de configuração do Systemd (`.service` e `.timer`). O *Timer* gerencia o agendamento de forma inteligente, garantindo que o script rode alguns minutos após o boot e se repita em intervalos definidos.

---

## ⚙️ Instalação e Configuração

Siga os passos abaixo para implantar a ferramenta no seu sistema:

### 1. Clonar o Repositório
```bash
git clone [https://github.com/SEU_USUARIO/Auto-Linux-Updater.git](https://github.com/SEU_USUARIO/Auto-Linux-Updater.git)
cd Auto-Linux-Updater
