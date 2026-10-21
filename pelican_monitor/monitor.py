import os
import json
import requests
import importlib

# Configurações do Telegram
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# Caminho para o arquivo de estado (IDs já processados)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(BASE_DIR, "processed_ids.json")

# Termos de busca
TERMS = ["pelican", "peli case", "maleta estanque pelican"]

# Quantos dias para trás consultar (Janela Ampliada)
DAYS_BACK = 7

# Lista de providers ativos a serem carregados dinamicamente da pasta providers/
ACTIVE_PROVIDERS = ['pncp', 'petronect', 'licitacoes_e', 'web_search']

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

def main():
    processed_ids = load_processed_ids()
    print(f"Iniciando monitoramento de editais para os termos {TERMS} (Últimos {DAYS_BACK} dias)")

    all_new_tenders = []
    success_count = 0

    for provider_name in ACTIVE_PROVIDERS:
        print(f"Executando provider: {provider_name}")
        try:
            module = importlib.import_module(f"providers.{provider_name}")
            # Retorna lista padronizada
            results = module.search(TERMS, days_back=DAYS_BACK)

            for item in results:
                item_id = item.get("id")
                if item_id and item_id not in processed_ids:
                    all_new_tenders.append(item)
                    processed_ids.add(item_id)

            success_count += 1
        except Exception as e:
            print(f"Falha global ao executar o provider {provider_name}: {e}")

    if not all_new_tenders:
        print(f"Nenhum novo edital encontrado. ({success_count}/{len(ACTIVE_PROVIDERS)} portais consultados com sucesso)")
    else:
        print(f"Foram encontrados {len(all_new_tenders)} novos editais. ({success_count}/{len(ACTIVE_PROVIDERS)} portais consultados com sucesso)")

        for tender in all_new_tenders:
            fonte = tender.get("source", "DESCONHECIDO")
            orgao = tender.get("orgao", "Órgão não informado")
            titulo = tender.get("title", "Título não informado")
            valor = tender.get("valor", "Não informado")
            link = tender.get("link", "")

            # Formatar valor se for numérico
            if isinstance(valor, (int, float)):
                valor = f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

            msg = (
                f"🚨 <b>Novo Edital Encontrado!</b>\n\n"
                f"🏢 <b>Fonte:</b> [{fonte}]\n"
                f"🏛 <b>Órgão/Empresa:</b> {orgao}\n"
                f"📄 <b>Objeto/Título:</b> {titulo}\n"
                f"💰 <b>Valor:</b> {valor}\n\n"
                f"🔗 <a href='{link}'>Acessar Oportunidade</a>"
            )

            send_telegram_message(msg)

    # Salvar estado atualizado
    save_processed_ids(processed_ids)
    print("Execução finalizada.")

if __name__ == "__main__":
    main()
