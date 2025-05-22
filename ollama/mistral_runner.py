# ollama/mistral_runner.py
"""
Chama Mistral 7B via Ollama REST para rerank.
"""
import requests
import time

def rerank_documents(query: str, docs: list) -> dict:
    """
    Realiza rerank com Mistral 7B via Ollama local.

    Args:
        query (str): Consulta do usuário.
        docs (list): Lista de dicionários contendo {"arquivo": ..., "conteudo": ...}

    Returns:
        dict: {"arquivo": str, "resumo": str}
    """
    prompt = build_prompt(query, docs)
    payload = {
        "model": "mistral:7b",
        "prompt": prompt,
        "stream": False
    }

    print("\n🔍 Prompt enviado ao Mistral:\n" + "=" * 60)
    print(prompt[:5000])  # Mostra apenas os primeiros 5000 caracteres do prompt
    print("=" * 60)

    for attempt in range(3):
        try:
            response = requests.post("http://localhost:11434/api/generate", json=payload, timeout=12)
            res = response.json().get("response", "")
            return parse_response(res, docs)
        except Exception as e:
            print(f"[Tentativa {attempt+1}] Erro: {e}")
            time.sleep(2 ** attempt)

    return {"arquivo": "", "resumo": ""}

def build_prompt(query: str, docs: list) -> str:
    prompt = f"A consulta do usuário foi:\n\"{query}\"\n\n"
    prompt += "Abaixo estão 5 documentos numerados de [1] a [5], com seus conteúdos integrais:\n\n"
    for i, doc in enumerate(docs[:5]):
        conteudo = doc["conteudo"].replace("\n", " ").strip()
        prompt += f"[{i+1}] {conteudo}\n\n"
    prompt += (
        "Com base na consulta do usuário, selecione o número do documento mais relevante entre os 5 apresentados.\n"
        "Responda apenas com:\n"
        "Linha 1: número do documento mais relevante (ex: [3])\n"
        "Linha 2-3: resumo com no máximo 2 linhas do conteúdo escolhido.\n"
        "Não adicione nenhum outro texto além dessas 3 linhas."
    )
    return prompt

def parse_response(texto: str, documentos: list) -> dict:
    """
    Interpreta a resposta do modelo.

    Args:
        texto (str): Texto bruto retornado do Ollama.
        documentos (list): Mesma lista enviada.

    Returns:
        dict: {"arquivo": str, "resumo": str}
    """
    linhas = texto.strip().splitlines()
    if not linhas or not linhas[0].startswith("["):
        print("⚠️ Resposta inesperada do modelo.")
        return {"arquivo": "", "resumo": ""}

    try:
        indice = int(linhas[0].strip("[]").strip())
        doc = documentos[indice]
        resumo = "\n".join(linhas[1:3]).strip()
        return {
            "arquivo": doc["arquivo"],
            "resumo": resumo
        }
    except Exception as e:
        print("❌ Erro ao interpretar resposta Mistral:", e)
        return {"arquivo": "", "resumo": ""}
