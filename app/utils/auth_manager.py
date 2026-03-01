import json
import os
import threading
import time
import base64
import hashlib
import secrets
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
from app.utils.config_manager import config_manager


class _CodeReceiver(BaseHTTPRequestHandler):
    server_version = "AuthCodeReceiver/1.0"
    code = None
    error = None

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path != "/callback":
            self.send_response(404)
            self.end_headers()
            return
        params = urllib.parse.parse_qs(parsed.query)
        if "error" in params:
            _CodeReceiver.error = params.get("error", ["unknown"])[0]
        elif "code" in params:
            _CodeReceiver.code = params["code"][0]
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"<html><body>Login completed. You can close this window.</body></html>")


class AuthManager:
    def __init__(self):
        self._oidc_config = None

    def _issuer(self):
        return config_manager.config.get("oidc_issuer_url", "https://account.ae-3803.com")

    def _client_id(self):
        return config_manager.config.get("oidc_client_id", "")

    def _redirect_port(self):
        return int(config_manager.config.get("oidc_redirect_port", 8765))

    def _scopes(self):
        return config_manager.config.get("oidc_scopes", "openid profile email offline_access")

    def load_oidc_config(self):
        issuer = self._issuer().rstrip("/")
        url = f"{issuer}/.well-known/openid-configuration"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        self._oidc_config = r.json()
        return self._oidc_config

    def is_authenticated(self):
        token = config_manager.config.get("access_token")
        exp = config_manager.config.get("expires_at")
        if not token or not exp:
            return False
        try:
            return time.time() < float(exp) - 30
        except Exception:
            return False

    def logout(self):
        for k in [
            "access_token",
            "refresh_token",
            "id_token",
            "expires_at",
            "user_sub",
            "user_name",
            "user_email",
            "user_picture",
        ]:
            if k in config_manager.config:
                del config_manager.config[k]
        config_manager.save_config()

    def _pkce_pair(self):
        verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b"=").decode()
        digest = hashlib.sha256(verifier.encode()).digest()
        challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
        return verifier, challenge

    def _start_receiver(self, port):
        _CodeReceiver.code = None
        _CodeReceiver.error = None
        httpd = HTTPServer(("127.0.0.1", port), _CodeReceiver)
        t = threading.Thread(target=httpd.handle_request, daemon=True)
        t.start()
        return httpd

    def login(self):
        if not self._oidc_config:
            self.load_oidc_config()
        client_id = self._client_id()
        if not client_id:
            raise RuntimeError("Client ID is required")
        port = self._redirect_port()
        redirect_uri = f"http://127.0.0.1:{port}/callback"
        verifier, challenge = self._pkce_pair()
        auth_url = self._oidc_config["authorization_endpoint"]
        state = base64.urlsafe_b64encode(secrets.token_bytes(16)).rstrip(b"=").decode()
        params = {
            "client_id": client_id,
            "response_type": "code",
            "redirect_uri": redirect_uri,
            "scope": self._scopes(),
            "code_challenge": challenge,
            "code_challenge_method": "S256",
            "state": state,
        }
        url = f"{auth_url}?{urllib.parse.urlencode(params)}"
        srv = self._start_receiver(port)
        webbrowser.open(url)
        deadline = time.time() + 300
        while time.time() < deadline and _CodeReceiver.code is None and _CodeReceiver.error is None:
            time.sleep(0.2)
        try:
            srv.server_close()
        except Exception:
            pass
        if _CodeReceiver.error:
            raise RuntimeError(_CodeReceiver.error)
        if not _CodeReceiver.code:
            raise RuntimeError("No authorization code received")
        code = _CodeReceiver.code
        token_url = self._oidc_config["token_endpoint"]
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "code_verifier": verifier,
        }
        r = requests.post(token_url, data=data, timeout=10)
        r.raise_for_status()
        token = r.json()
        access_token = token.get("access_token")
        id_token = token.get("id_token")
        refresh_token = token.get("refresh_token")
        expires_in = token.get("expires_in", 3600)
        config_manager.config["access_token"] = access_token
        config_manager.config["id_token"] = id_token
        if refresh_token:
            config_manager.config["refresh_token"] = refresh_token
        config_manager.config["expires_at"] = time.time() + float(expires_in)
        config_manager.save_config()
        self._fetch_userinfo()
        return True

    def _fetch_userinfo(self):
        if not self._oidc_config:
            self.load_oidc_config()
        url = self._oidc_config.get("userinfo_endpoint")
        token = config_manager.config.get("access_token")
        if not url or not token:
            return
        r = requests.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=10)
        if r.status_code != 200:
            return
        info = r.json()
        if "sub" in info:
            config_manager.config["user_sub"] = info.get("sub")
        if "name" in info:
            config_manager.config["user_name"] = info.get("name")
        if "email" in info:
            config_manager.config["user_email"] = info.get("email")
        if "picture" in info:
            config_manager.config["user_picture"] = info.get("picture")
        if "name" in info and info.get("name"):
            config_manager.config["username"] = info.get("name")
        config_manager.save_config()


auth_manager = AuthManager()
