#!/usr/bin/env python3
"""
VIVANT Plain Text Bot Template
Production template for Plain Text Mode (guest@) with auto-reconnect and room rotation.
"""

import os
import re
import sys
import time
import logging
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("vivant_bot")

SSH_HOST = os.environ.get("VIVANT_HOST", "term.freedom8964.com")
SSH_PORT = os.environ.get("VIVANT_PORT", "2222")
SSH_USER = os.environ.get("VIVANT_USER", "guest")
NICKNAME = os.environ.get("VIVANT_NICK", "my_bot")
ROOMS = ["general", "chinese", "technology", "english", "anonymous"]

RE_DM = re.compile(r"^\[\d{2}:\d{2}\]\s+\[(?:私信|DM|私聊).*?[←<-]\s*([^\]]+)\]\s*(.*)$")
RE_CROSS_ROOM = re.compile(r"^\[\d{2}:\d{2}\]\s+@\s*#(\w+)\s+<([^>]+)>\s*(.*)$")
RE_ROOM_MSG = re.compile(r"^\[\d{2}:\d{2}\]\s+<([^>]+)>\s*(.*)$")
RE_ROOM_ENTERED = re.compile(r"已进入\s*#(\w+)|Now in\s*#(\w+)")

class VivantBot:
    def __init__(self, nickname=NICKNAME, rotate_sec=30):
        self.proc = None
        self.nickname = nickname
        self.rotate_sec = rotate_sec
        self.write_lock = threading.Lock()
        self.room_idx = 0
        self.current_room = ROOMS[0]
        self.in_backlog = True
        self.executor = ThreadPoolExecutor(max_workers=3)
        self.running = True
        self.last_rotate = time.time()

    def send(self, cmd):
        with self.write_lock:
            if self.proc and self.proc.stdin:
                try:
                    self.proc.stdin.write(cmd + "\n")
                    self.proc.stdin.flush()
                except Exception as e:
                    logger.error("Failed to send: %s", e)

    def on_message(self, sender, text, msg_type, source_room=None):
        logger.info("[%s] %s: %s", msg_type, sender, text)
        if f"@{self.nickname.lower()}" in text.lower():
            reply = f"Hello {sender}! I am online."
            if msg_type == "dm":
                self.send(f"/msg {sender} {reply}")
            elif msg_type == "cross_room":
                self.send(f"/msg {sender} @{sender} {reply}")
            else:
                self.send(f"@{sender} {reply}")

    def on_line(self, line):
        line = line.strip()
        if not line:
            return

        if RE_ROOM_ENTERED.search(line):
            self.in_backlog = False
            return

        m_dm = RE_DM.match(line)
        if m_dm:
            sender, text = m_dm.group(1).strip(), m_dm.group(2).strip()
            if sender.lower() != self.nickname.lower():
                self.executor.submit(self.on_message, sender, text, "dm")
            return

        m_cross = RE_CROSS_ROOM.match(line)
        if m_cross:
            room, sender, text = m_cross.group(1).strip(), m_cross.group(2).strip(), m_cross.group(3).strip()
            text = re.sub(r"\s*·\s*/join\s+\S+", "", text).strip()
            if sender.lower() != self.nickname.lower():
                self.executor.submit(self.on_message, sender, text, "cross_room", room)
            return

        m_room = RE_ROOM_MSG.match(line)
        if m_room:
            sender, text = m_room.group(1).strip(), m_room.group(2).strip()
            text = re.sub(r"^[»\s]+", "", text).strip()
            if sender.lower() == self.nickname.lower() or self.in_backlog:
                return
            self.executor.submit(self.on_message, sender, text, "room")
            return

    def run_session(self):
        cmd = [
            "ssh",
            "-o", "StrictHostKeyChecking=no",
            "-o", "UserKnownHostsFile=/dev/null",
            "-o", "ServerAliveInterval=15",
            "-o", "ServerAliveCountMax=3",
            "-o", "ConnectTimeout=10",
            "-o", "LogLevel=ERROR",
            "-p", str(SSH_PORT),
            f"{SSH_USER}@{SSH_HOST}"
        ]
        logger.info("Connecting to %s:%s...", SSH_HOST, SSH_PORT)
        self.proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        time.sleep(2)
        self.send(f"/nick {self.nickname}")
        self.in_backlog = True

        try:
            for line in self.proc.stdout:
                self.on_line(line)
        finally:
            try:
                self.proc.terminate()
            except Exception:
                pass
            self.proc = None

    def start(self):
        while self.running:
            try:
                self.run_session()
            except Exception as e:
                logger.error("Session crash: %s", e)
            logger.info("Reconnecting in 5s...")
            time.sleep(5)

if __name__ == "__main__":
    bot = VivantBot()
    bot.start()
