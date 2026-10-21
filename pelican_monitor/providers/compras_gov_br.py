import requests
import hashlib
from datetime import datetime, timedelta
import pytz
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

BRT = pytz.timezone('America/Sao_Paulo')

def create_session():
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

def search(terms, days_back=7):
    """
    Busca na API de Dados Abertos do Compras.gov.br (Antigo Comprasnet).
    Endpoint público de licitações: https://dadosabertos.compras.gov.br/modulo-licitacoes/3_doc_api.html
    (Nota: Se a API exigir parâmetros diferentes em produção, este é um scraper best-effort)
    """
    results = []
    session = create_session()

    # Exemplo de endpoint público do SIASG/ComprasGov
    # Muitas vezes, esses dados estão na api de /licitacoes/v1/
    url = "https://compras.dados.gov.br/licitacoes/v1/licitacoes.json"

    now = datetime.now(BRT)
    # Compras.gov.br data format often is YYYY-MM-DD
    min_date = (now - timedelta(days=days_back)).strftime("%Y-%m-%d")

    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        # A API do Compras.gov.br historicamente suporta o parâmetro 'item' ou 'objeto'
        # para busca textual, mas muitas vezes a busca é feita iterando as do dia.
        # Faremos uma query simplificada 'best-effort' por data
        params = {
            "data_publicacao": min_date
        }

        response = session.get(url, params=params, headers=headers, timeout=15)

        if response.status_code == 200:
            data = response.json()
            embedded = data.get("_embedded", {}).get("licitacoes", [])

            for item in embedded:
                objeto = item.get("objeto", "")

                # Filtrar em memória caso a API não tenha text search full na rota de licitações
                match_found = False
                for term in terms:
                    if term.lower() in objeto.lower():
                        match_found = True
                        matched_term = term
                        break

                if not match_found:
                    continue

                uasg = item.get("uasg", "Não informado")
                num_licitacao = item.get("numero_aviso", "Não informado")
                link = f"http://comprasnet.gov.br/ConsultaLicitacoes/download/download_editais_detalhe.asp?qtuasg={uasg}&modprp=5&numprp={num_licitacao}"

                ident = str(item.get("identificador", ""))
                if not ident:
                    ident = hashlib.md5((uasg + str(num_licitacao)).encode('utf-8')).hexdigest()

                results.append({
                    "id": f"cnet_{ident}",
                    "title": f"Pregão Eletrônico {num_licitacao} - UASG {uasg}",
                    "description": objeto,
                    "orgao": f"UASG {uasg}",
                    "process_number": num_licitacao,
                    "link": link,
                    "valor": "Não informado",
                    "prazo": item.get("data_entrega_edital", "Não informado"),
                    "status": item.get("situacao_aviso", "Aberto"),
                    "term": matched_term,
                    "source": "COMPRAS.GOV.BR"
                })
    except Exception as e:
        print(f"[COMPRAS.GOV.BR] Erro ao buscar: {e}")

    return results
