from google.cloud import firestore
import google.cloud.logging
import logging
from .config import PROJECT_ID, FIRESTORE_COLLECTION
from datetime import datetime, timezone

# Initialize Google Cloud Logging
try:
    logging_client = google.cloud.logging.Client(project=PROJECT_ID)
    logging_client.setup_logging()
except Exception as e:
    # Fallback to standard logging if not in GCP
    logging.basicConfig(level=logging.INFO)
    logging.warning(f"Could not setup Google Cloud Logging, using standard logging: {e}")

logger = logging.getLogger("bot_logger")

def get_firestore_client():
    try:
        return firestore.Client(project=PROJECT_ID)
    except Exception as e:
        logger.error(f"Error initializing Firestore Client: {e}")
        return None

def log_trade(tweet_data: dict, analysis_result: dict, execution_result: dict = None, status: str = "PENDING"):
    """
    Logs the full context of a trade event into Firestore for traceability.
    """
    db = get_firestore_client()
    if not db:
        logger.error("Firestore client not available. Cannot log trade to database.")
        return

    log_entry = {
        "timestamp": datetime.now(timezone.utc),
        "tweet_id": tweet_data.get("id"),
        "author_id": tweet_data.get("author_id"),
        "tweet_text": tweet_data.get("text"),
        "analysis": analysis_result,
        "execution": execution_result,
        "status": status  # PENDING, EXECUTED, REJECTED, FAILED
    }

    try:
        doc_ref = db.collection(FIRESTORE_COLLECTION).document()
        doc_ref.set(log_entry)
        logger.info(f"Successfully logged trade event for tweet {tweet_data.get('id')} with status {status}.")
    except Exception as e:
        logger.error(f"Failed to write to Firestore: {e}")
