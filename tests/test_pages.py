import http.server
import socketserver
import threading
import functools
import requests
from pathlib import Path
import time

import pytest

@pytest.fixture(scope="module")
def http_server():
    # Serve files from repository root
    root = Path(__file__).resolve().parents[1]
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(root))
    httpd = socketserver.TCPServer(("localhost", 0), handler)
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    # Wait a moment for server to start
    time.sleep(0.1)
    yield f"http://localhost:{port}"
    httpd.shutdown()
    thread.join()

def check_page(base_url, page, keyword):
    resp = requests.get(f"{base_url}/{page}")
    assert resp.status_code == 200
    assert keyword in resp.text

def test_ramais(http_server):
    check_page(http_server, "ramais.html", "Ramais e Telefones")

def test_cadastro_empresas(http_server):
    check_page(http_server, "cadastro-empresas.html", "Cadastro das Empresas")

def test_whatsapp(http_server):
    check_page(http_server, "whatsapp.html", "Contatos de WhatsApp")
