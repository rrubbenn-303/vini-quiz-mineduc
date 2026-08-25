# Trading Bot Trump - High-Speed Crypto Trading

Este repositorio contiene la estructura base para un bot de trading de criptomonedas de alta velocidad que opera en OKX basándose en tweets en tiempo real de la familia Trump.

## Arquitectura

El proyecto utiliza una arquitectura serverless asíncrona en Google Cloud Platform (GCP) para minimizar la latencia:

1. **Ingester (`src/ingester.py`)**: Microservicio (FastAPI) desplegado en Cloud Run. Recibe los webhooks de X (Twitter), valida que provengan de las cuentas objetivo, y publica el payload en Pub/Sub.
2. **Pub/Sub**: Desacopla la recepción del procesamiento, asegurando que ningún evento se pierda por picos de tráfico.
3. **Processor (`src/processor.py`)**: Script trabajador que escucha mensajes de Pub/Sub.
4. **Analyzer (`src/analyzer.py`)**: Utiliza Gemini (vía `google-genai`) para realizar NLP sobre el tweet, devolviendo un JSON estructurado (Pydantic) para decidir si operar.
5. **Risk Manager (`src/risk.py`)**: Filtra por límite de capital (50 USDT por orden) y aplica un cooldown de 60s entre operaciones.
6. **Executor (`src/executor.py`)**: Utiliza `ccxt` para ejecutar órdenes en OKX (configurado en modo Sandbox por defecto).
7. **Database (`src/database.py`)**: Registra la trazabilidad completa en Google Cloud Firestore y Logs.

## Requisitos Previos

- Cuenta en Google Cloud Platform (GCP)
- API Keys de OKX (con permisos de trading)
- API Key de X (Twitter) para webhooks
- API Key de Google Gemini (Google AI Studio)

## Despliegue en GCP

### 1. Configurar Secret Manager
Crea los siguientes secretos en Google Cloud Secret Manager:
- `OKX_API_KEY`
- `OKX_API_SECRET`
- `OKX_API_PASSWORD`
- `TWITTER_BEARER_TOKEN`
- `GEMINI_API_KEY`

Asegúrate de otorgar el rol `Secret Manager Secret Accessor` a la cuenta de servicio que ejecutará los contenedores.

### 2. Configurar Pub/Sub
Crea un tema (`topic`) llamado `tweet-ingestion-topic` y una suscripción asociada llamada `tweet-processor-sub`.

### 3. Configurar Firestore
Inicializa una base de datos de Firestore en modo Nativo en tu proyecto de GCP.

### 4. Desplegar Ingester en Cloud Run
Desde la raíz del proyecto, despliega la API de ingesta:

```bash
gcloud run deploy tweet-ingester --source . --allow-unauthenticated
```
Configura la URL resultante como tu endpoint en la API de webhooks de X.

### 5. Desplegar el Processor
El archivo `src/processor.py` funciona como un suscriptor de Pub/Sub (Pull).
Para un entorno de producción, se recomienda ejecutar este script en una instancia de Compute Engine pequeña (e2-micro) o configurarlo en Cloud Run como un Job de ejecución continua (Always-on).

Para probarlo localmente (con tus credenciales de GCP configuradas):
```bash
python -m src.processor
```

## Pruebas Locales

1. Crea un entorno virtual e instala las dependencias: `pip install -r requirements.txt`
2. Copia `.env.example` a `.env` y rellena tus claves de prueba.
3. Asegúrate de estar autenticado en GCP (`gcloud auth application-default login`).
4. Inicia el ingester: `uvicorn src.ingester:app --reload`
5. En otra terminal, inicia el procesador: `python -m src.processor`
