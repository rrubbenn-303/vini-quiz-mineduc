import requests
from datetime import datetime, timedelta
import pytz

BRT = pytz.timezone('America/Sao_Paulo')

def search(terms, days_back=7):
    """
    Busca editais no PNCP.
    Retorna lista de dicts: [{"id", "title", "orgao", "link", "valor", "term", "source"}]
    """
    results = []

    # Calcular as datas na janela de dias
    now = datetime.now(BRT)
    dates_to_search = []
    for i in range(days_back):
        d = now - timedelta(days=i)
        # Formato YYYYMMDD para a API do PNCP (data_inicial e data_final)
        date_api_str = d.strftime("%Y%m%d")
        # Formato retornado no JSON para validação
        date_filter_str = d.strftime("%Y-%m-%d")
        dates_to_search.append((date_api_str, date_filter_str))

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }

    url = "https://pncp.gov.br/api/search"

    for term in terms:
        for date_api, date_str in dates_to_search:
            params = {
                "q": term,
                "tipos_documento": "edital",
                "data_inicial": date_api,
                "data_final": date_api
            }
            try:
                response = requests.get(url, params=params, headers=headers, timeout=30)
                if response.status_code == 200:
                    items = response.json().get("items", [])
                    for item in items:
                        item_id = item.get("id")
                        data_pub = item.get("data_publicacao_pncp", "")

                        # Garantir que bate com a data que estamos buscando (para evitar lixo)
                        if not data_pub.startswith(date_str):
                            continue

                        if not item_id:
                            continue

                        # Extrair informações
                        orgao = item.get("orgao_nome", "Órgão não informado")
                        titulo = item.get("title", "Edital")
                        objeto = item.get("description", "Objeto não informado")
                        valor = item.get("valor_total_estimado") or item.get("valor_total_homologado") or "Não informado"

                        # Formatar URL
                        item_url = item.get("item_url", "")
                        if item_url.startswith("/"):
                            link = f"https://pncp.gov.br/app/editais{item_url}"
                        else:
                            link = "https://pncp.gov.br"

                        results.append({
                            "id": f"pncp_{item_id}",
                            "title": f"{titulo} - {objeto}",
                            "orgao": orgao,
                            "link": link,
                            "valor": valor,
                            "term": term,
                            "source": "PNCP"
                        })
            except Exception as e:
                print(f"[PNCP] Erro ao buscar termo '{term}' na data {date_api}: {e}")

    return results
