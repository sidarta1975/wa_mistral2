# search_service.py
"""
Seleciona o documento mais relevante do base_modelos.jsonl com rerank pelo Mistral.
"""
import os
import json
from glossario.enriquecedor import enriquecer_query
from ollama.mistral_runner import rerank_documents

CAMINHO_JSONL = "data/base_modelos.jsonl"

def carregar_jsonl() -> list:
    if not os.path.exists(CAMINHO_JSONL):
        raise FileNotFoundError("base_modelos.jsonl não encontrado.")
    with open(CAMINHO_JSONL, "r", encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]

def handle_query(query: str) -> dict:
    print("\n🧠 Consulta recebida:", query)

    documentos = carregar_jsonl()
    print("📁 Documentos carregados:", len(documentos))

    consulta_expandida = enriquecer_query(query)
    print("🔎 Consulta expandida:", consulta_expandida)

    docs_completos = [doc for doc in documentos if isinstance(doc.get("conteudo"), str)]
    resposta = rerank_documents(consulta_expandida, docs_completos)

    if not resposta or not resposta.get("arquivo"):
        print("⚠️ Nenhum documento retornado pelo Mistral.")
        return {"error": "Nenhum documento encontrado."}

    doc_escolhido = next((d for d in docs_completos if d["arquivo"] == resposta["arquivo"]), None)
    if not doc_escolhido:
        print("⚠️ Documento indicado pelo Mistral não localizado.")
        return {"error": "Documento indicado não encontrado."}

    print("✅ Documento selecionado:", doc_escolhido["arquivo"])
    return {
        "caminho": doc_escolhido["arquivo"],
        "nome_arquivo": doc_escolhido["arquivo"],
        "resumo": "",
        "conteudo": doc_escolhido["conteudo"]
    }
