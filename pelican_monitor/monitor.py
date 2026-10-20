import os
import json
import requests
from datetime import datetime
import pytz

# Configurações do Telegram
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# Caminho para o arquivo de estado (IDs já processados)
# O caminho é relativo à pasta do script para rodar corretamente no Github Actions
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(BASE_DIR, "processed_ids.json")

# Termos de busca
TERMS = ["pelican", "peli case", "maleta estanque pelican"]

# Fuso horário de Brasília
BRT = pytz.timezone('America/Sao_Paulo')

def load_processed_ids():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            try:
                return set(json.load(f))
            except json.JSONDecodeError:
                return set()
    return set()

def save_processed_ids(ids):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(list(ids), f, indent=2)

def send_telegram_message(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Aviso: Configurações do Telegram (TOKEN ou CHAT_ID) não encontradas.")
        print("Mensagem que seria enviada:", message)
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

def get_today_date_str():
    # Retorna YYYYMMDD para uso no filtro da API (se suportado)
    # E YYYY-MM-DD para filtro manual
    now = datetime.now(BRT)
    return now.strftime("%Y%m%d"), now.strftime("%Y-%m-%d")

def fetch_tenders(query, date_api_str):
    url = "https://pncp.gov.br/api/search"
    params = {
        "q": query,
        "tipos_documento": "edital",
        "data_inicial": date_api_str,
        "data_final": date_api_str
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        if response.status_code == 200:
            return response.json().get("items", [])
        else:
            print(f"Erro na API PNCP para termo '{query}': {response.status_code} - {response.text}")
            return []
    except Exception as e:
        print(f"Exceção ao acessar API PNCP para termo '{query}': {e}")
        return []

def main():
    processed_ids = load_processed_ids()
    date_api_str, date_filter_str = get_today_date_str()
    print(f"Executando monitoramento para o dia {date_filter_str} (Brasília)")

    new_tenders = []

    for term in TERMS:
        print(f"Buscando por: {term}")
        items = fetch_tenders(term, date_api_str)

        for item in items:
            item_id = item.get("id")

            # Filtro extra no lado do cliente para garantir que seja da data atual
            # formato retornado: '2024-10-24T15:10:04.430509'
            data_pub = item.get("data_publicacao_pncp", "")

            if not data_pub.startswith(date_filter_str):
                continue

            if item_id and item_id not in processed_ids:
                new_tenders.append(item)
                processed_ids.add(item_id)

    if not new_tenders:
        print("Nenhum novo edital encontrado para os termos buscados hoje.")
    else:
        for tender in new_tenders:
            orgao = tender.get("orgao_nome", "Órgão não informado")
            objeto = tender.get("description", "Objeto não informado")
            valor = tender.get("valor_total_estimado") or tender.get("valor_total_homologado") or "Não informado"

            # Formatar valor se for numérico
            if isinstance(valor, (int, float)):
                valor = f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

            # Construir URL do PNCP. Algumas vêm em 'item_url' como rota relativa.
            item_url = tender.get("item_url", "")
            if item_url.startswith("/"):
                url = f"https://pncp.gov.br/app/editais{item_url}"
            else:
                url = "https://pncp.gov.br"

            titulo = tender.get("title", "Edital")

            msg = (
                f"🚨 <b>Novo Edital Encontrado!</b>\n\n"
                f"🏢 <b>Órgão:</b> {orgao}\n"
                f"📄 <b>Título:</b> {titulo}\n"
                f"📝 <b>Objeto:</b> {objeto}\n"
                f"💰 <b>Valor Estimado:</b> {valor}\n\n"
                f"🔗 <a href='{url}'>Acessar Edital no PNCP</a>"
            )

            send_telegram_message(msg)

    # Salvar estado no arquivo
    save_processed_ids(processed_ids)
    print("Execução finalizada.")

if __name__ == "__main__":
    main()
