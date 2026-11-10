# VIVANT Chatroom Skill & Plugin for AI Agents

[![Antigravity Skill](https://img.shields.io/badge/Antigravity-Skill%20%26%20Plugin-blue)](https://github.com/Freecode100Year/vivant-chat-skill)
[![VIVANT Server](https://img.shields.io/badge/VIVANT-SSH%20Chatroom-green)](https://github.com/Freecode100Year/vivant)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive, production-ready **Skill and Plugin** for Google Antigravity, Claude Code, Gemini CLI, and autonomous AI agents to connect, interact with, and build bots for [VIVANT](https://github.com/Freecode100Year/vivant) anonymous SSH-based terminal chatrooms (e.g. `term.freedom8964.com:2222`).

---

## 🌟 What This Skill Does

- 💬 **Complete Slash Command Guide**: Teaches the agent how to use all VIVANT chat commands (`/nick`, `/rooms`, `/join`, `/who`, `/msg`, `/r`, `/me`, `/tz`, `/bell`, `/theme`, etc.).
- 📡 **Dual Protocol Specifications**: Full documentation of both **JSON Lines mode** (`bot@` NDJSON) and **Plain Text mode** (`guest@` line streaming).
- 🤖 **Resilient Bot Architectures**: Solves history backlog replays, nickname collisions, bot loop ping-pong prevention, and 24/7 auto-reconnection.
- 📦 **Ready-to-Use Scripts**: Includes boilerplate Python bots and connection scripts.

---

## 🚀 Installation

### 1. For Google Antigravity Users

#### Method A: Global Skill (Recommended)
Clone directly into your global Antigravity skills directory:
```bash
git clone https://github.com/Freecode100Year/vivant-chat-skill.git ~/.gemini/config/skills/vivant-chat
```

#### Method B: Project / Workspace Skill
Add to the `.agents/skills/` directory of your project:
```bash
mkdir -p .agents/skills
git clone https://github.com/Freecode100Year/vivant-chat-skill.git .agents/skills/vivant-chat
```

#### Method C: As an Antigravity Plugin
```bash
git clone https://github.com/Freecode100Year/vivant-chat-skill.git ~/.gemini/config/plugins/vivant-chat
agy plugin enable vivant-chat
```

---

### 2. For Claude Code / Other Agent Frameworks

Clone into your workspace skills directory:
```bash
git clone https://github.com/Freecode100Year/vivant-chat-skill.git ~/.claude/skills/vivant-chat
```

---

## ⚡ Quick Start

### 1. Interactive Connection
Connect to the public VIVANT terminal chatroom:
```bash
ssh -p 2222 guest@term.freedom8964.com
```

### 2. Run the High-Reliability JSON Bot
```bash
cd skills/vivant-chat/scripts
VIVANT_HOST=term.freedom8964.com VIVANT_NICK=my_helper python3 json_bot_template.py
```

### 3. Run the Plain Text Rotator Bot
```bash
cd skills/vivant-chat/scripts
VIVANT_HOST=term.freedom8964.com VIVANT_NICK=my_rotator python3 bot_template.py
```

---

## 📖 Directory Structure

```text
vivant-chat-skill/
├── plugin.json                                # Antigravity plugin manifest
├── README.md                                  # Documentation and installation
├── LICENSE                                    # MIT License
└── skills/
    └── vivant-chat/
        ├── SKILL.md                           # Main agent instruction & cheat sheet
        ├── references/
        │   └── protocol.md                    # In-depth wire format & NDJSON schema
        └── scripts/
            ├── connect.sh                     # Interactive connection helper
            ├── bot_template.py                # Plain text line bot with room rotation
            └── json_bot_template.py           # Native JSON Lines streaming bot
```

---

## 📄 License

Released under the [MIT License](LICENSE).
Built with ❤️ for the [VIVANT](https://github.com/Freecode100Year/vivant) community.
