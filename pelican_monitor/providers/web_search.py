import hashlib
from ddgs import DDGS

def search(terms, days_back=7):
    """
    Busca menções recentes aos termos na web.
    Filtro anti-ruído forte aplicado nativamente nas queries para duckduckgo.
    """
    results = []

    # Lista enxuta de queries rotativas de alto impacto para evitar rate limit
    queries = [
        '"pelican" (licitação OR pregão OR cotação OR aquisição) -nba -basketball -filme -caneta',
        '"case pelican" (licitação OR aquisição OR cotação) -nba',
        '"maleta pelican" (licitação OR aquisição OR cotação)',
        '"maleta estanque" (licitação OR aquisição OR cotação)',
        '"lanterna pelican" OR "lanterna atex" (licitação OR aquisição)',
        '"pelican 1510" OR "pelican 1560" OR "pelican 1650" (licitação OR aquisição OR cotação)'
    ]

    # days_back = 7 map para DuckDuckGo time='w' (past week)
    time_filter = "w" if days_back <= 7 else "m"

    try:
        ddgs = DDGS()
        for query in queries:
            try:
                search_results = list(ddgs.text(query, region='br-pt', safesearch='off', timelimit=time_filter, max_results=3))

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
                        "description": snippet,
                        "orgao": "Desconhecido (Busca Web)",
                        "link": link,
                        "valor": "Não informado",
                        "prazo": "Não informado",
                        "status": "Aberto (Web)",
                        "term": "Busca Otimizada",
                        "source": "WEB SEARCH"
                    })
            except Exception as e:
                print(f"[WEB_SEARCH] Erro na query '{query}': {e}")
    except Exception as e:
        print(f"[WEB_SEARCH] Erro fatal no DDGS: {e}")

    return results
