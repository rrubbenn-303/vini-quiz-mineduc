from typing import Optional
from pydantic import BaseModel, Field
from google import genai
from .config import load_secrets
from .database import logger

# Initialize Gemini Client (lazy load on first call to ensure secrets are ready)
_genai_client = None

def get_genai_client():
    global _genai_client
    if not _genai_client:
        secrets = load_secrets()
        api_key = secrets.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set or couldn't be loaded.")
        _genai_client = genai.Client(api_key=api_key)
    return _genai_client

class TweetAnalysisResult(BaseModel):
    trade: bool = Field(description="Whether the tweet warrants a trading operation.")
    symbol: Optional[str] = Field(description="The crypto asset to trade, formatted as BASE/QUOTE (e.g., 'BTC/USDT', 'WLFI/USDT'). Null if no trade.")
    action: Optional[str] = Field(description="The action to take: 'BUY' or 'SELL'. Null if no trade.")
    confidence: float = Field(description="Confidence level of the analysis, from 0.0 to 1.0.")

def analyze_tweet(tweet_text: str) -> TweetAnalysisResult:
    """
    Analyzes a tweet using Gemini 3.7 Flash and returns a structured output.
    """
    prompt = f"""
    Analyze the following tweet and determine if it suggests a clear and immediate trading opportunity in the cryptocurrency market.
    Focus on major cryptocurrencies or tokens explicitly mentioned (e.g., Bitcoin, Ethereum, WLFI).
    Ignore irrelevant mentions, retweets without commercial impact, or general political statements that do not directly imply an action on a specific asset.
    If it's a clear signal to buy or sell, set 'trade' to true, specify the 'symbol' (e.g., BTC/USDT), and the 'action' (BUY or SELL).
    Calculate a 'confidence' score between 0.0 and 1.0 based on how explicit the signal is.

    Tweet: "{tweet_text}"
    """

    try:
        client = get_genai_client()
        # Using Gemini 3.7 Flash model as requested for low latency
        response = client.models.generate_content(
            model='gemini-2.5-flash', # Since gemini 3.7 flash is a typo and doesnt exist yet, fallback to gemini-2.5-flash or gemini-2.0-flash, we will use gemini-2.5-flash as the latest fast model
            contents=prompt,
            config={
                'response_mime_type': 'application/json',
                'response_schema': TweetAnalysisResult,
                'temperature': 0.1 # Low temperature for more deterministic output
            },
        )

        # The SDK returns the parsed pydantic object directly if configured correctly
        # But just in case, we parse it
        import json
        result_dict = json.loads(response.text)
        analysis = TweetAnalysisResult(**result_dict)
        logger.info(f"Analysis result: {analysis.model_dump()}")
        return analysis

    except Exception as e:
        logger.error(f"Error analyzing tweet with Gemini: {e}")
        # Default fallback to avoid taking action on errors
        return TweetAnalysisResult(trade=False, symbol=None, action=None, confidence=0.0)
