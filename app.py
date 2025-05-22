# app.py
"""
API Flask para consulta de petições via modelo Mistral.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from search.search_service import handle_query

app = Flask(__name__)
CORS(app)

@app.route("/buscar", methods=["POST"])
def buscar_documento():
    try:
        data = request.get_json()
        if not data or "query" not in data:
            print("❌ Requisição sem JSON válido ou sem campo 'query'.")
            return jsonify({"error": "Requisição inválida: campo 'query' ausente."}), 400

        query = data.get("query", "").strip()
        if not query:
            print("❌ Consulta vazia recebida.")
            return jsonify({"error": "Consulta vazia."}), 400

        print("🔎 Requisição recebida com consulta:", query)
        resultado = handle_query(query)

        if "error" in resultado:
            print("⚠️ Erro no processamento:", resultado["error"])
            return jsonify(resultado), 404

        print("✅ Resultado retornado:", resultado.get("nome_arquivo"))
        return jsonify(resultado)

    except Exception as e:
        print("❌ Erro inesperado na API:", e)
        return jsonify({"error": "Erro interno no servidor."}), 500

if __name__ == "__main__":
    app.run(debug=True)
