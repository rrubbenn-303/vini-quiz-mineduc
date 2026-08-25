import json
import time
from google.cloud import pubsub_v1
from src.config import PROJECT_ID, PUBSUB_SUBSCRIPTION_NAME
from src.database import logger, log_trade
from src.analyzer import analyze_tweet
from src.risk import validate_trade_risk, update_cooldown
from src.executor import execute_trade, get_current_price

def process_message(message: pubsub_v1.subscriber.message.Message):
    """
    Callback function to process incoming messages from Pub/Sub.
    Orchestrates the Analyzer, Risk Manager, and Executor.
    """
    try:
        # 1. Parse Message
        payload = message.data.decode("utf-8")
        tweet_data = json.loads(payload)
        tweet_text = tweet_data.get("text", "")

        logger.info(f"Processing tweet {tweet_data.get('id')}: {tweet_text[:50]}...")

        # 2. Analyze with Gemini
        analysis = analyze_tweet(tweet_text)

        if not analysis.trade or not analysis.symbol or not analysis.action:
            logger.info("Analyzer decided not to trade. Ignoring.")
            log_trade(tweet_data, analysis.model_dump(), status="REJECTED_BY_AI")
            message.ack()
            return

        # 3. Check current price
        current_price = get_current_price(analysis.symbol)
        if current_price <= 0:
            logger.error("Failed to fetch valid price. Aborting.")
            log_trade(tweet_data, analysis.model_dump(), status="FAILED_PRICE_FETCH")
            message.ack()
            return

        # 4. Validate Risk and Calculate Size/SL/TP
        risk_result = validate_trade_risk(analysis.symbol, analysis.action, current_price)

        if not risk_result["approved"]:
            logger.warning(f"Trade rejected by Risk Manager: {risk_result['reason']}")
            log_trade(tweet_data, analysis.model_dump(), execution_result=risk_result, status="REJECTED_BY_RISK")
            message.ack()
            return

        # 5. Execute Trade
        execution_result = execute_trade(
            symbol=analysis.symbol,
            action=analysis.action,
            size=risk_result["size"],
            stop_loss=risk_result["stop_loss"],
            take_profit=risk_result["take_profit"]
        )

        # 6. Post-execution steps
        if execution_result["status"] == "success":
            update_cooldown(analysis.symbol)
            log_trade(tweet_data, analysis.model_dump(), execution_result=execution_result, status="EXECUTED")
        else:
            log_trade(tweet_data, analysis.model_dump(), execution_result=execution_result, status="FAILED_EXECUTION")

    except Exception as e:
        logger.error(f"Error processing message: {e}")
        # We might want to nack() to retry, but for tweets, usually better to ack and log to avoid poison pills
    finally:
        # Acknowledge the message so it's not redelivered
        message.ack()

def start_processor():
    """
    Starts the Pub/Sub subscriber to listen for messages continuously.
    """
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(PROJECT_ID, PUBSUB_SUBSCRIPTION_NAME)

    logger.info(f"Starting processor, listening to {subscription_path}")

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=process_message)

    try:
        # Block the main thread to keep the subscriber running
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()
        logger.info("Processor stopped manually.")
    except Exception as e:
        logger.error(f"Processor encountered an error: {e}")
        streaming_pull_future.cancel()

if __name__ == "__main__":
    start_processor()
