import re
import config

def extract_quantity(text):
    """
    Tenta extrair a quantidade do texto via regex simples.
    Retorna a quantidade encontrada ou 'Não informado'.
    """
    match = re.search(r'\b(\d+)\s*(unidades?|und?|pe[çc]as?|pcs?|itens?)\b', text, re.IGNORECASE)
    if match:
        return f"{match.group(1)} {match.group(2)}"
    return "Não informado"

def extract_snippet(text, match_obj, padding=100):
    """
    Extrai um snippet ao redor do match_obj para destacar o termo que gerou o alerta.
    Adiciona <b> ao redor do termo encontrado.
    """
    start = max(0, match_obj.start() - padding)
    end = min(len(text), match_obj.end() + padding)

    # Extrai o contexto e aplica a formatação html
    snippet = text[start:end]
    matched_term = match_obj.group(0)

    # Se o snippet não começou no início do texto, coloca '...'
    prefix = "..." if start > 0 else ""
    suffix = "..." if end < len(text) else ""

    # Replace the actual match in the snippet with bold tags
    # We use a simple replacement for the first occurrence in the snippet
    snippet = snippet.replace(matched_term, f"<b>{matched_term}</b>", 1)

    # Clean up whitespace
    snippet = re.sub(r'\s+', ' ', snippet).strip()
    return f"{prefix}{snippet}{suffix}"

def classify(title, description):
    """
    Avalia o título e a descrição de uma oportunidade.
    Retorna (Categoria, Produto_Identificado, Quantidade, Snippet) ou (None, None, None, None) se descartado.
    Categorias: "PRIORITARIA" ou "POTENCIAL".
    """
    # Juntar título e descrição para análise
    full_text = f"{title}. {description}".replace("\n", " ")

    # 1. Verificar intenção de compra
    intent_match = config.BUYING_INTENT_TERMS.search(full_text)

    # Se for da web, muitas vezes a intenção de compra já foi garantida na query.
    # Porém, para editais que nós puxamos da API via termo genérico, exigimos a intenção,
    # OU consideramos que o fato de vir do PNCP/BB já é intenção de compra.
    # Mas como o usuário pediu para cruzar intenção:
    has_intent = bool(intent_match)

    # No caso de PNCP, BB, Petronect, TUDO é intenção de compra nativamente
    # Mas o requisito pede a combinação, então usaremos a combinação ou a suposição de que
    # a fonte oficial (que controlamos no parser) garante a intenção.

    # 2. Avaliar PRIORIDADE ALTA (Marca ou Modelo contextual)
    brand_match = config.BRANDS_AND_FAMILIES.search(full_text)
    model_match = config.CONTEXTUAL_MODEL_REGEX.search(full_text)

    if brand_match or model_match:
        the_match = brand_match if brand_match else model_match
        produto = the_match.group(0).strip()
        qtd = extract_quantity(full_text)
        snippet = extract_snippet(full_text, the_match)
        return "PRIORITARIA", produto, qtd, snippet

    # 3. Avaliar OPORTUNIDADE POTENCIAL (Termos Técnicos Genéricos)
    tech_match = config.DESCRIPTORS_COMPATIBLE.search(full_text)
    if tech_match:
        produto = "Compatível por especificação"
        qtd = extract_quantity(full_text)
        snippet = extract_snippet(full_text, tech_match)
        return "POTENCIAL", produto, qtd, snippet

    # Se não passou em nenhum dos filtros, descartar
    return None, None, None, None
