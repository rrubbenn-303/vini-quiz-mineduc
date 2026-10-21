import os
import json
import importlib

import config
import classifier
import telegram

# Caminho para o arquivo de estado (IDs já processados)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(BASE_DIR, "processed_ids.json")

# Quantos dias para trás consultar (Janela Ampliada)
DAYS_BACK = 7

# Lista de providers ativos a serem carregados dinamicamente da pasta providers/
ACTIVE_PROVIDERS = [
    'pncp',
    'compras_gov_br',
    'licitacoes_e',
    'bec_sp',
    'bll_compras',
    'portal_compras_publicas',
    'petronect',
    'mercado_eletronico'
]

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

def main():
    processed_ids = load_processed_ids()
    print(f"Iniciando monitoramento de editais para os termos base {config.SEED_TERMS_API} (Últimos {DAYS_BACK} dias)")

    success_count = 0
    notificacoes_enviadas = 0

    for provider_name in ACTIVE_PROVIDERS:
        print(f"Executando provider: {provider_name}")
        try:
            module = importlib.import_module(f"providers.{provider_name}")

            # Para o web_search, os termos já estão otimizados lá dentro.
            # Para os outros, passamos a semente SEED_TERMS_API
            results = module.search(config.SEED_TERMS_API, days_back=DAYS_BACK)

            for item in results:
                item_id = item.get("id")

                # Só processa se for novo
                if item_id and item_id not in processed_ids:

                    # Classificação Inteligente
                    categoria, produto, qtd, snippet = classifier.classify(item)

                    if categoria:
                        msg = telegram.format_alert(item, categoria, produto, qtd, snippet)
                        telegram.send_message(msg)
                        notificacoes_enviadas += 1

                    # Independentemente se foi descartado ou notificado, adiciona para não re-analisar
                    processed_ids.add(item_id)

            success_count += 1
        except Exception as e:
            print(f"Falha global ao executar o provider {provider_name}: {e}")

    print(f"Foram avaliados e salvos novos IDs. ({notificacoes_enviadas} notificações enviadas, {success_count}/{len(ACTIVE_PROVIDERS)} portais consultados com sucesso)")

    # Salvar estado atualizado
    save_processed_ids(processed_ids)
    print("Execução finalizada.")

if __name__ == "__main__":
    main()
