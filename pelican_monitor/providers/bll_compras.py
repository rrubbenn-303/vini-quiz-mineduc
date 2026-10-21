import requests

def search(terms, days_back=7):
    """
    Busca na BLL Compras.
    Best-effort scraper. Retorna array vazio em caso de erro.
    """
    results = []
    url = "https://bllcompras.com/Process/ProcessSearch"

    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        pass
    except Exception as e:
        print(f"[BLL_COMPRAS] Erro ao buscar: {e}")

    return results
