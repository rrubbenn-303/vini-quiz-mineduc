import requests
from bs4 import BeautifulSoup
import hashlib

def search(terms, days_back=7):
    """
    Busca menções recentes aos termos no Licitações-e (Banco do Brasil).
    Retorna lista de dicts padronizada.

    A busca no portal do BB frequentemente requer navegação com estado e post forms.
    Fazemos um scraper best-effort tolerante a falhas.
    """
    results = []

    # URL da busca pública de licitações-e
    url = "https://www.licitacoes-e.com.br/aop/pesquisar-licitacao.aop"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
    }

    for term in terms:
        try:
            # Em um cenário real de scraping do ASP/JSP do Licitações-e,
            # usaríamos um payload com dados como 'numeroLicitacao', 'termoPesquisa', etc.
            payload = {
                "opcaoPesquisa": "3", # Opção por objeto
                "termoPesquisa": term
            }

            response = requests.post(url, data=payload, headers=headers, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Exemplo hipotético de estrutura do HTML do BB
                rows = soup.find_all('tr', class_='linha-tabela')
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) > 3:
                        orgao = cols[0].text.strip()
                        titulo = cols[1].text.strip()
                        link_tag = cols[1].find('a')
                        link = f"https://www.licitacoes-e.com.br{link_tag['href']}" if link_tag else url

                        item_id = f"lice_{hashlib.md5(link.encode('utf-8')).hexdigest()}"

                        results.append({
                            "id": item_id,
                            "title": titulo,
                            "orgao": orgao,
                            "link": link,
                            "valor": "Não informado",
                            "term": term,
                            "source": "LICITAÇÕES-E"
                        })
        except Exception as e:
            print(f"[LICITAÇÕES-E] Erro ao buscar termo '{term}': {e}")

    return results
