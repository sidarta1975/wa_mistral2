# tests/test_app.py
"""
Testa a API Flask local da aplicação.
"""

import pytest
from app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_buscar_documento_valido(client):
    response = client.post("/buscar", json={"query": "guarda compartilhada"})
    data = response.get_json()

    assert response.status_code == 200
    assert "caminho" in data
    assert "resumo" in data


def test_buscar_documento_vazio(client):
    response = client.post("/buscar", json={"query": ""})
    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == "Consulta vazia."
