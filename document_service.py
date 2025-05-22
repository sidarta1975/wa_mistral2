# document_service.py

"""
Serviço de extração do documento mais relevante para uma consulta.
Integra com a lógica de rerank via handle_query (search_service).
"""

from search.search_service import handle_query
from typing import Dict, Optional

def find_relevant_documents(query: str) -> Dict[str, Optional[str]]:
    """
    Usa rerank para encontrar o documento relevante e lê o conteúdo completo.

    Args:
        query (str): Consulta do usuário.

    Returns:
        dict: {"nome_arquivo": str, "conteudo": str} ou valores None caso falhe
    """
    try:
        resultado = handle_query(query)
        caminho = resultado.get("caminho", "")

        if not caminho:
            return {
                "nome_arquivo": None,
                "conteudo": None
            }

        return {
            "nome_arquivo": resultado.get("nome_arquivo"),
            "conteudo": resultado.get("conteudo")
        }

    except Exception as e:
        print(f"[document_service] Erro ao buscar documento: {e}")
        return {
            "nome_arquivo": None,
            "conteudo": None
        }
