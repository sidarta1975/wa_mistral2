# glossario/enriquecedor.py
"""
Enriquece a query com referência semântica, se termo estiver no glossário.
"""

from glossario.glossary_loader import carregar_termos_glossario

# Caminho atualizado para a versão atual do glossário
CAMINHO_GLOSSARIO = "glossario/glossario.tsv"

TERMS = carregar_termos_glossario(CAMINHO_GLOSSARIO)

def enriquecer_query(query: str) -> str:
    """
    Expande semanticamente a consulta do usuário com base nos termos do glossário.

    Args:
        query (str): Texto da pergunta feita pelo usuário.

    Returns:
        str: Consulta original com nota explicativa, se aplicável.
    """
    q_lower = query.lower()

    for termo in TERMS:
        termo_clean = termo.strip().lower()
        if termo_clean in q_lower:
            return f"{query}\n(NOTA: o termo '{termo}' consta no glossário jurídico e deve ser considerado com atenção especial.)"

    return query
