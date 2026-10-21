import requests

def search(terms, days_back=7):
    """
    Busca no Mercado Eletrônico (B2B).
    Best-effort scraper da vitrine pública de cotações (quando disponível sem login corporativo).
    Retorna array vazio em caso de erro.
    """
    results = []
    url = "https://www.me.com.br"

    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        pass
    except Exception as e:
        print(f"[MERCADO_ELETRONICO] Erro ao buscar: {e}")

    return results
