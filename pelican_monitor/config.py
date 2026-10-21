import re

# Termos raiz para consultar nas APIs do PNCP, Petronect e Licitacoes-e
SEED_TERMS_API = [
    "pelican", "peli case", "maleta estanque", "maleta hermetica",
    "caixa estanque", "lanterna intrinsecamente segura",
    "lanterna atex", "sistema de iluminacao portatil"
]

# Regex para Marcas e Famílias
BRANDS_AND_FAMILIES = re.compile(
    r"\b(pelican(?: case)?|peli|case pelican|maleta pelican|caixa pelican|lanterna pelican|protector|air|vault|storm|hardigg|micro case)\b",
    re.IGNORECASE
)

# Regex para Modelos de Cases
# Grupo 1: Pequenos a Grandes e Longos
# Grupo 2: Vault
# Grupo 3: ATX/HC
_MODELS_CASES_PATTERN = r"\b(0915|0945|0955|0965|GO\s*5|M40|M50|M60|1010|1020|1120|1150|1200|1300|1400|1430|1440|1450|1460|1485|1500|1505|1507|1510|1520|1525|1535|1550|1555|1556|1557|1560|1595|1600|1605|1607|1610|1615|1620|1630|1637|1640|1650|1660|1690|1700|1720|1730|1740|1745|1750|1755|1770|1780|0340|0370|0450|0500|0550)\b(?:-?\s*(NF|WD|TP|SC|M|LOC|LFC|CC1|EMS|TRVL|TRAVEL))?|\b(V-?\s*(?:100|200|250|300|525|550|600|700|730|770|800))\b|\b(ATX\s*(?:22|25|30)|HC(?:22|25|30))\b"
MODELS_CASES = re.compile(_MODELS_CASES_PATTERN, re.IGNORECASE)

# Regex para Lanternas
MODELS_LIGHTS = re.compile(
    r"\b(1975-?i|2010-?i|2410|2690|2745|2755|2765|3315|3335-?R|3610|9415-?i|9455)\b",
    re.IGNORECASE
)

# Regex para proximidade (janela de até 8 palavras) de modelos numéricos para validar se são realmente Pelican
# Contextos aceitos: pelican, peli, case, maleta, mala, caixa, lanterna
CONTEXT_WORDS = r"(pelican|peli|case|maleta|mala|caixa|lanterna)"
# Modelos numéricos que precisam de contexto: basicamente qualquer número listado acima
# Essa regex detecta se um modelo numérico está perto das palavras de contexto (antes ou depois)
CONTEXTUAL_MODEL_REGEX = re.compile(
    rf"(?:{CONTEXT_WORDS}(?:\W+\w+){{0,8}}\W+(?:{_MODELS_CASES_PATTERN}|(1975-?i|2010-?i|2410|2690|2745|2755|2765|3315|3335-?R|3610|9415-?i|9455))|(?:{_MODELS_CASES_PATTERN}|(1975-?i|2010-?i|2410|2690|2745|2755|2765|3315|3335-?R|3610|9415-?i|9455))(?:\W+\w+){{0,8}}\W+{CONTEXT_WORDS})",
    re.IGNORECASE
)

# Descritores compatíveis (genéricos)
DESCRIPTORS_COMPATIBLE = re.compile(
    r"\b(case r[ií]gido|maleta r[ií]gida|caixa estanque|maleta estanque|v[aá]lvula de equaliza[cç][aã]o|espuma pr[eé]-cortada|espuma picotada|IP67|seguran[cç]a intr[ií]nseca|atmosfera explosiva|antideflagrante|Ex ia|IECEx|torre de ilumina[cç][aã]o port[aá]til)\b",
    re.IGNORECASE
)

# Intenção de compra
BUYING_INTENT_TERMS = re.compile(
    r"\b(licita[cç][aã]o|preg[aã]o|dispensa de licita[cç][aã]o|dispensa eletr[oô]nica|edital|termo de refer[eê]ncia|aquisi[cç][aã]o|cota[cç][aã]o|solicita[cç][aã]o de or[cç]amento|registro de pre[cç]os|RFQ|RFP|comprar)\b",
    re.IGNORECASE
)

# Termos negativos para Web Search (Apenas como string para uso na Query DDGS)
NEGATIVE_WEB_TERMS = "-nba -basketball -filme -movie -caneta -cupom -desconto -pelikano -venda -promoção"
