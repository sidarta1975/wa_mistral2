# whatsapp_connector.py
"""
Simula um conector WhatsApp com ativação por palavra-chave "advogada parceira".
"""

from conversation import process_query
from logger import setup_logger

logger = setup_logger(__name__)

# Estado por usuário (se está em diálogo ou não)
active_users = {}

def initialize_whatsapp():
    """
    Inicia a simulação do bot.
    """
    print("🤖 Simulação WhatsApp iniciada. Digite 'advogada parceira' para ativar.")
    while True:
        raw = input("Usuário> ").strip()
        if raw.lower() in ["exit", "sair", "q", "quit"]:
            print("👋 Encerrando simulação.")
            break
        simulate_incoming_message("simulacao@grupo", raw)

def simulate_incoming_message(user_id: str, message: str):
    """
    Simula recebimento de mensagem e gerencia estado de ativação.

    Args:
        user_id (str): ID do remetente
        message (str): Mensagem de entrada
    """
    logger.info(f"📨 [{user_id}] {message}")
    message_lower = message.lower()

    # Inicializa estado do usuário se necessário
    if user_id not in active_users:
        active_users[user_id] = False

    # Ativação
    if not active_users[user_id]:
        if "advogada parceira" in message_lower:
            active_users[user_id] = True
            send_text_message(user_id, "Olá, qual petição você precisa? Pode me falar o nome da petição ou o assunto.")
        else:
            logger.info(f"Ignorando mensagem fora do contexto de ativação: {user_id}")
        return

    # Resposta com petição
    if active_users[user_id]:
        resposta = process_query(user_id, message)
        send_text_message(user_id, resposta)

        # Mensagem final e encerramento
        send_text_message(user_id, "Se precisar de outra petição, digite 'advogada parceira' novamente.")
        active_users[user_id] = False
        logger.info(f"Conversa com {user_id} encerrada após entrega.")

def send_text_message(to: str, text: str):
    """
    Simula envio de texto ao WhatsApp.

    Args:
        to (str): ID do destinatário
        text (str): Mensagem a enviar
    """
    print(f"\n[ENVIADO para {to}]\n{text}\n")

if __name__ == "__main__":
    initialize_whatsapp()
