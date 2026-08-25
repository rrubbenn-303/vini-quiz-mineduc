import os
from google.cloud import secretmanager

# Google Cloud configuration
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-project-id")

# Target Twitter IDs
TARGET_TWITTER_IDS = [
    25073877,            # @realDonaldTrump
    39344374,            # @DonaldJTrumpJr
    1367531,             # @EricTrump
    1831411516091490304  # @worldlibertyfi and other official projects
]

# Pub/Sub Configuration
PUBSUB_TOPIC_NAME = "tweet-ingestion-topic"
PUBSUB_SUBSCRIPTION_NAME = "tweet-processor-sub"

# Risk Management
MAX_CAPITAL_PER_ORDER_USDT = 50.0
COOLDOWN_SECONDS = 60

# Firestore Configuration
FIRESTORE_COLLECTION = "trade_logs"

def get_secret(secret_id: str, version_id: str = "latest") -> str:
    """
    Retrieves a secret from Google Cloud Secret Manager.
    Uses local environment variables if present for local testing.
    """
    # Prefer local env var for testing (set in .env)
    if os.environ.get(secret_id):
        return os.environ.get(secret_id)

    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/{version_id}"

    try:
        response = client.access_secret_version(request={"name": name})
        secret_payload = response.payload.data.decode("UTF-8")
        return secret_payload
    except Exception as e:
        print(f"Error accessing secret {secret_id}: {e}")
        return ""

def load_secrets():
    """
    Load all required secrets.
    """
    return {
        "OKX_API_KEY": get_secret("OKX_API_KEY"),
        "OKX_API_SECRET": get_secret("OKX_API_SECRET"),
        "OKX_API_PASSWORD": get_secret("OKX_API_PASSWORD"),
        "TWITTER_BEARER_TOKEN": get_secret("TWITTER_BEARER_TOKEN"),
        "GEMINI_API_KEY": get_secret("GEMINI_API_KEY")
    }
