import hashlib
from ddgs import DDGS

def search(terms, days_back=7):
    """
    Busca menções recentes aos termos na web.
    Filtro anti-ruído forte aplicado nativamente nas queries para duckduckgo.
    """
    results = []

    # Termos e palavras negativas focadas no contexto brasileiro e de hardware
    refined_terms = ['"maleta pelican"', '"case pelican"', '"maleta estanque pelican"']
    buying_keywords = ['cotação', 'aquisição', 'orçamento', 'licitação', 'comprar']
    negative_words = '-nba -basketball -filme -movie -caneta -cupom -desconto -pelikano'

    # days_back = 7 map para DuckDuckGo time='w' (past week)
    time_filter = "w" if days_back <= 7 else "m"

    try:
        ddgs = DDGS()
        for r_term in refined_terms:
            for kw in buying_keywords:
                query = f'{r_term} {kw} {negative_words}'
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
                            "orgao": "Desconhecido (Busca Web)",
                            "link": link,
                            "valor": "Não informado",
                            "term": r_term.replace('"', ''),
                            "source": "WEB SEARCH"
                        })
                except Exception as e:
                    print(f"[WEB_SEARCH] Erro na query '{query}': {e}")
    except Exception as e:
        print(f"[WEB_SEARCH] Erro fatal no DDGS: {e}")

    return results
