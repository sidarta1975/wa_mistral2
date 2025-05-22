# scripts/construir_jsonl.py
"""
Gera o arquivo base_modelos.jsonl a partir de /templates e /glossario.
Evita duplicatas por hash, associa termos do glossário e calcula metadados.
"""
import os
import json
import hashlib
from datetime import datetime
from glob import glob
from glossario.glossary_loader import carregar_termos_glossario
from glossario.enriquecedor import enriquecer_query

TEMPLATES_DIR = "templates"
SAIDA_JSONL = "data/base_modelos.jsonl"

def hash_conteudo(texto: str) -> str:
    return hashlib.sha256(texto.strip().encode("utf-8")).hexdigest()

def estimar_tokens(texto: str) -> int:
    return int(len(texto.split()) * 1.3)

def carregar_hashes_existentes(path: str) -> set:
    if not os.path.exists(path):
        return set()
    with open(path, "r", encoding="utf-8") as f:
        return {json.loads(l)["hash_conteudo"] for l in f if l.strip()}

def processar_arquivo(path_txt: str, termos_glossario: list) -> dict:
    with open(path_txt, "r", encoding="utf-8") as f:
        conteudo = f.read().strip()

    hash_doc = hash_conteudo(conteudo)
    termos_encontrados = [t for t in termos_glossario if t.lower() in conteudo.lower()]

    return {
        "arquivo": os.path.basename(path_txt),
        "conteudo": conteudo,
        "hash_conteudo": hash_doc,
        "glossario": termos_encontrados,
        "tamanho_tokens": estimar_tokens(conteudo),
        "data_processado": datetime.now().isoformat(),
        "verificado": False,
        "comentarios": [],
        "blocos": {
            "peca": None,
            "justica": None,
            "enderecamento": None,
            "fatos": None,
            "fundamentos": None,
            "legislacao": None,
            "jurisprudencia": None,
            "pedidos": None
        }
    }

def main():
    os.makedirs("data", exist_ok=True)
    termos = carregar_termos_glossario("glossario/glossario.tsv")
    hashes_existentes = carregar_hashes_existentes(SAIDA_JSONL)

    novos = 0
    with open(SAIDA_JSONL, "a", encoding="utf-8") as f:
        for path in glob(f"{TEMPLATES_DIR}/*.txt"):
            doc = processar_arquivo(path, termos)
            if doc["hash_conteudo"] in hashes_existentes:
                continue
            f.write(json.dumps(doc, ensure_ascii=False) + "\n")
            novos += 1

    print(f"✅ {novos} novos documentos adicionados a {SAIDA_JSONL}")

if __name__ == "__main__":
    main()
