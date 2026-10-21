import requests

def search(terms, days_back=7):
    """
    Busca no Portal de Compras Públicas.
    Best-effort scraper. Retorna array vazio em caso de erro.
    """
    results = []
    url = "https://www.portaldecompraspublicas.com.br/processos"

    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        pass
    except Exception as e:
        print(f"[PORTAL_COMPRAS_PUBLICAS] Erro ao buscar: {e}")

    return results
