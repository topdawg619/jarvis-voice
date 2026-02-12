#!/usr/bin/env python3
"""Tiny static server for the Jarvis voice config file.

Serves a single JSON payload with permissive CORS headers so the
GitHub Pages client can fetch https://<tunnel>/jarvis-voice-config.json.

Usage:
  python3 tools/static_config_server.py

Optional env vars:
  JARVIS_VOICE_CONFIG_PATH   absolute path to the JSON file
                             (default: /home/csmith/.openclaw/private/jarvis-voice-config.json)
  JARVIS_VOICE_CONFIG_HOST   host/IP to bind (default: 127.0.0.1)
  JARVIS_VOICE_CONFIG_PORT   port to bind (default: 9001)
"""

from __future__ import annotations

import http.server
import os
import pathlib
import socketserver
from typing import Tuple

CONFIG_PATH = pathlib.Path(
    os.environ.get(
        "JARVIS_VOICE_CONFIG_PATH",
        "/home/csmith/.openclaw/private/jarvis-voice-config.json",
    )
)
HOST = os.environ.get("JARVIS_VOICE_CONFIG_HOST", "127.0.0.1")
PORT = int(os.environ.get("JARVIS_VOICE_CONFIG_PORT", "9001"))


class ConfigHandler(http.server.BaseHTTPRequestHandler):
    server_version = "JarvisConfigServer/0.1"

    def log_message(self, fmt: str, *args):  # noqa: D401
        """Send logs to stdout like http.server does."""
        print("[config-server]" , fmt % args)

    def _load_config(self) -> bytes:
        if not CONFIG_PATH.exists():
            raise FileNotFoundError(
                f"config file missing: {CONFIG_PATH}. Fill it before starting."
            )
        return CONFIG_PATH.read_bytes()

    def do_GET(self):  # noqa: N802
        if self.path not in ("/jarvis-voice-config.json", "/"):
            self.send_error(404, "Not Found")
            return
        try:
            payload = self._load_config()
        except FileNotFoundError as exc:
            self.send_error(500, str(exc))
            return
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


def serve():
    with socketserver.TCPServer((HOST, PORT), ConfigHandler) as httpd:
        url = f"http://{HOST}:{PORT}/jarvis-voice-config.json"
        print(f"Serving {CONFIG_PATH} at {url}")
        httpd.serve_forever()


if __name__ == "__main__":
    serve()
