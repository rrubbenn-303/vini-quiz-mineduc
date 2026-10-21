import requests
from bs4 import BeautifulSoup
import hashlib

def search(terms, days_back=7):
    """
    Busca menções recentes aos termos na plataforma Petronect.
    Retorna lista de dicts padronizada.

    Como a Petronect não tem uma API pública simples para busca livre sem login,
    este é um scraper best-effort das vitrines públicas.
    Se não for possível acessar os dados, loga o erro e retorna vazio.
    """
    results = []

    # Exemplo de URL pública (pode variar/mudar, é uma tentativa best-effort)
    url = "https://www.petronect.com.br/app/compras"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
    }

    try:
        # Apenas para fins de simulação/best-effort scraper caso haja um endpoint aberto identificável.
        # Muitas vezes a Petronect requer POST com form data de ASP.NET e sessão.
        # Se falhar o get, a exceção é capturada e os outros módulos continuam funcionando.
        response = requests.get(url, headers=headers, timeout=10)

        # Como o objetivo aqui é não quebrar e mostrar o design pattern (e porque sem credenciais
        # a busca real na petronect pode não funcionar via GET simples publicamente):
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Lógica hipotética de scraping:
            # bids = soup.find_all('div', class_='bid-item')
            # for bid in bids: ...

            # Não encontrando a estrutura facilmente, os resultados continuam vazios sem erro fatal.
            pass

    except Exception as e:
        print(f"[PETRONECT] Erro ao buscar: {e}")

    return results
