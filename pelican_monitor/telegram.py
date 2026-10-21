import os
import requests

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_message(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Aviso: Configurações do Telegram (TOKEN ou CHAT_ID) não encontradas.")
        print("Mensagem que seria enviada:\n", message)
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        print("Mensagem enviada com sucesso para o Telegram.")
    except Exception as e:
        print(f"Erro ao enviar mensagem para o Telegram: {e}")

def format_alert(tender, category, produto, qtd, snippet):
    """
    Formata a mensagem para o Telegram baseado nas regras do projeto.
    """
    icone = "🚨" if category == "PRIORITARIA" else "⚠️"
    tipo_alerta = "ALERTA PRIORITÁRIO: MARCA/MODELO PELICAN" if category == "PRIORITARIA" else "OPORTUNIDADE COMPATÍVEL: REQUER REVISÃO TÉCNICA"

    fonte = tender.get("source", "Desconhecido")
    orgao = tender.get("orgao", "Não informado")

    valor = tender.get("valor", "Não informado")
    if isinstance(valor, (int, float)):
        valor = f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    data_prazo = tender.get("prazo", "Não informado")
    status = tender.get("status", "Aberto")
    link = tender.get("link", "")

    msg = (
        f"{icone} <b>{tipo_alerta}</b>\n\n"
        f"🏢 <b>Órgão / Comprador:</b> {orgao} [{fonte}]\n"
        f"📦 <b>Produto / Modelo Identificado:</b> {produto}\n"
        f"🔢 <b>Quantidade:</b> {qtd}\n"
        f"💰 <b>Valor (Total/Unitário):</b> {valor}\n"
        f"📅 <b>Data / Prazo de Resposta:</b> {data_prazo}\n"
        f"📌 <b>Status:</b> {status}\n\n"
        f"📝 <b>Trecho identificado:</b>\n"
        f"<i>\"{snippet}\"</i>\n\n"
        f"🔗 <a href='{link}'>Acessar Edital / Oportunidade</a>"
    )

    return msg
