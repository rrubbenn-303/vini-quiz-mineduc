import hashlib
from ddgs import DDGS

def search(terms, days_back=7):
    """
    Busca menções recentes aos termos na web combinados com palavras-chave de licitação.
    Utiliza o DuckDuckGo Search (gratuito).
    """
    results = []

    keywords = ['licitação', 'pregão', 'edital', 'compras']

    # days_back = 7 map para DuckDuckGo time='w' (past week)
    time_filter = "w" if days_back <= 7 else "m"

    try:
        ddgs = DDGS()
        for term in terms:
            for kw in keywords:
                query = f'"{term}" {kw}'
                try:
                    # Buscamos poucos resultados (max_results=5) para não sobrecarregar
                    search_results = list(ddgs.text(query, region='br-pt', safesearch='off', timelimit=time_filter, max_results=5))

                    for r in search_results:
                        title = r.get("title", "")
                        link = r.get("href", "")
                        snippet = r.get("body", "")

                        if not link:
                            continue

                        # Gerar um ID único baseado na URL
                        url_hash = hashlib.md5(link.encode('utf-8')).hexdigest()
                        item_id = f"web_{url_hash}"

                        results.append({
                            "id": item_id,
                            "title": title,
                            "orgao": "Desconhecido (Busca Web)",
                            "link": link,
                            "valor": "Não informado",
                            "term": term,
                            "source": "WEB SEARCH"
                        })
                except Exception as e:
                    print(f"[WEB_SEARCH] Erro na query '{query}': {e}")
    except Exception as e:
        print(f"[WEB_SEARCH] Erro fatal no DDGS: {e}")

    return results
