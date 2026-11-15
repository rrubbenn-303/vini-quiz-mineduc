import json
from fastapi import FastAPI, Request, HTTPException
from google.cloud import pubsub_v1
from src.config import PROJECT_ID, PUBSUB_TOPIC_NAME, TARGET_TWITTER_IDS
from src.database import logger

app = FastAPI(title="Twitter Webhook Ingester")

# Initialize Pub/Sub Publisher
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, PUBSUB_TOPIC_NAME)

@app.post("/webhook")
async def receive_tweet(request: Request):
    """
    Webhook endpoint to receive incoming tweets.
    Validates if the author is in our target list and publishes to Pub/Sub.
    """
    try:
        data = await request.json()
    except Exception as e:
        logger.error(f"Invalid JSON received: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON")

    # Adapt this extraction based on the exact format of the incoming webhook (X API or third-party)
    # Assuming a simplified standard format:
    tweet_id = data.get("id")
    author_id = data.get("author_id")

    if not tweet_id or not author_id:
        logger.warning(f"Malformed payload received: {data}")
        return {"status": "ignored", "reason": "Missing id or author_id"}

    try:
        author_id_int = int(author_id)
    except ValueError:
        logger.warning(f"Non-integer author_id received: {author_id}")
        return {"status": "ignored", "reason": "Invalid author_id format"}

    # Filter by target authors
    if author_id_int not in TARGET_TWITTER_IDS:
        logger.info(f"Ignored tweet from non-target author_id: {author_id}")
        return {"status": "ignored", "reason": "Author not in target list"}

    # Publish to Pub/Sub
    try:
        payload_bytes = json.dumps(data).encode("utf-8")
        future = publisher.publish(topic_path, data=payload_bytes)
        message_id = future.result()
        logger.info(f"Published tweet {tweet_id} to Pub/Sub with message ID {message_id}")
        return {"status": "success", "message_id": message_id}
    except Exception as e:
        logger.error(f"Error publishing to Pub/Sub: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/health")
def health_check():
    return {"status": "ok"}
