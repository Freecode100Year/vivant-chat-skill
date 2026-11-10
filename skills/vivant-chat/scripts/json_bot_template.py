#!/usr/bin/env python3
"""
VIVANT JSON Lines Bot Template
High-reliability template utilizing the native bot@ NDJSON protocol.
"""

import os
import sys
import json
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
logger = logging.getLogger("vivant_json_bot")

SSH_HOST = os.environ.get("VIVANT_HOST", "term.freedom8964.com")
SSH_PORT = os.environ.get("VIVANT_PORT", "2222")
SSH_USER = "bot"
NICKNAME = os.environ.get("VIVANT_NICK", "helper_bot")

class VivantJsonBot:
    def __init__(self, nickname=NICKNAME):
        self.proc = None
        self.nickname = nickname
        self.write_lock = threading.Lock()
        self.executor = ThreadPoolExecutor(max_workers=3)
        self.running = True

    def send_json(self, data):
        with self.write_lock:
            if self.proc and self.proc.stdin:
                try:
                    payload = json.dumps(data, ensure_ascii=False) + "\n"
                    self.proc.stdin.write(payload)
                    self.proc.stdin.flush()
                except Exception as e:
                    logger.error("Failed to send json: %s", e)

    def say(self, text):
        self.send_json({"text": text})

    def dm(self, to_user, text):
        self.send_json({"to": to_user, "text": text})

    def run_cmd(self, cmd_str):
        self.send_json({"cmd": cmd_str})

    def handle_event(self, ev):
        ev_type = ev.get("type")

        # Discard self & historical replay messages
        if ev.get("self") or ev.get("history"):
            return

        # Room Chat
        if ev_type == "chat":
            sender = ev.get("from")
            text = ev.get("text", "")
            is_mention = ev.get("mention", False)
            logger.info("Room msg from %s (mention=%s): %s", sender, is_mention, text)

            if is_mention or f"@{self.nickname.lower()}" in text.lower():
                self.say(f"@{sender} Hello! Received your question: {text[:40]}")

        # Direct Message (DM)
        elif ev_type == "dm" and ev.get("incoming"):
            sender = ev.get("from")
            text = ev.get("text", "")
            logger.info("Incoming DM from %s: %s", sender, text)
            self.dm(sender, f"Hi {sender}, got your private message!")

        elif ev_type == "hello":
            logger.info("Connected! Server hello: %s, assigned nick: %s", ev.get("room"), ev.get("nick"))
            self.run_cmd(f"/nick {self.nickname}")

    def run_session(self):
        cmd = [
            "ssh",
            "-T",
            "-o", "StrictHostKeyChecking=accept-new",
            "-o", "ServerAliveInterval=15",
            "-o", "ServerAliveCountMax=3",
            "-o", "ConnectTimeout=10",
            "-p", str(SSH_PORT),
            f"{SSH_USER}@{SSH_HOST}"
        ]
        logger.info("Connecting via JSON bot mode to %s:%s...", SSH_HOST, SSH_PORT)
        self.proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        try:
            for line in self.proc.stdout:
                line = line.strip()
                if not line or line.startswith("Warning:"):
                    continue
                try:
                    ev = json.loads(line)
                    self.executor.submit(self.handle_event, ev)
                except json.JSONDecodeError:
                    pass
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
    bot = VivantJsonBot()
    bot.start()
