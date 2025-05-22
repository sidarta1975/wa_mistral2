# tests/test_document_service.py
import os
from document_service import find_relevant_documents
from unittest.mock import patch

@patch("document_service.handle_query")
def test_find_relevant_documents_lendo_txt(mock_handle_query, tmp_path):
    fake_txt = tmp_path / "modelo.txt"
    fake_txt.write_text("Petição teste integral.")

    mock_handle_query.return_value = {
        "nome_arquivo": str(fake_txt.name),
        "conteudo": "Petição teste integral.",
        "resumo": "Resumo simulado."
    }
    resultado = find_relevant_documents("guarda compartilhada")
    assert resultado is not None
    assert "Petição" in resultado["conteudo"]
