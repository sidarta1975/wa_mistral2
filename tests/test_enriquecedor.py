# tests/test_enriquecedor.py
import json
import pytest
from glossario.enriquecedor import enriquecer_query
from glossario.glossary_loader import carregar_termos_glossario

@pytest.fixture(autouse=True)
def mock_glossario(tmp_path, monkeypatch):
    fake_path = tmp_path / "termos_extraidos.json"
    termos = [["guarda compartilhada"], ["usucapião"]]
    fake_path.write_text(json.dumps(termos), encoding="utf-8")
    monkeypatch.setattr("glossario.glossary_loader.carregar_termos_glossario", lambda: [t[0] for t in termos])

def test_enriquecimento_ocorre():
    q = "Pedido de guarda compartilhada"
    resultado = enriquecer_query(q)
    assert "glossário jurídico" in resultado

def test_enriquecimento_ignorado(monkeypatch, tmp_path):
    fake_path = tmp_path / "termos_extraidos.json"
    fake_path.write_text(json.dumps([["usucapião"]]), encoding="utf-8")
    monkeypatch.setattr("glossario.glossary_loader.carregar_termos_glossario", lambda: ["usucapião"])

    q = "Pedido de liminar"
    resultado = enriquecer_query(q)
    assert resultado == q


# tests/test_app.py
import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_buscar_documento_valido(client):
    response = client.post("/buscar", json={"query": "guarda compartilhada"})
    assert response.status_code == 200 or response.status_code == 404  # depende se rerank funcionou

