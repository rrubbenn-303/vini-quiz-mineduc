import requests
import hashlib

def search(terms, days_back=7):
    """
    Busca na Bolsa Eletrônica de Compras do Estado de SP (BEC-SP).
    Best-effort scraper - sem credenciais, muitas vezes portais governamentais bloqueiam bots.
    Retorna array vazio em caso de erro.
    """
    results = []
    url = "https://www.bec.sp.gov.br/bec_sp_ui/aspx/becsp_pesquisa_publica.aspx"

    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        # Implementação placeholder best-effort para extração com BeautifulSoup
        pass
    except Exception as e:
        print(f"[BEC_SP] Erro ao buscar: {e}")

    return results
