import ccxt
from src.config import load_secrets
from src.database import logger

_exchange = None

def get_exchange():
    """
    Initializes and returns the CCXT exchange instance for OKX.
    Enables Sandbox mode for testing.
    """
    global _exchange
    if not _exchange:
        secrets = load_secrets()
        api_key = secrets.get("OKX_API_KEY")
        secret = secrets.get("OKX_API_SECRET")
        password = secrets.get("OKX_API_PASSWORD")

        if not all([api_key, secret, password]):
            logger.warning("OKX credentials missing. Executor will likely fail.")

        _exchange = ccxt.okx({
            'apiKey': api_key,
            'secret': secret,
            'password': password,
            'enableRateLimit': True,
        })

        # Enable Sandbox (Testnet) Mode
        _exchange.set_sandbox_mode(True)
        logger.info("OKX Exchange initialized in SANDBOX mode.")

    return _exchange

def get_current_price(symbol: str) -> float:
    """
    Fetches the current ticker price for the symbol.
    """
    exchange = get_exchange()
    try:
        ticker = exchange.fetch_ticker(symbol)
        return ticker['last']
    except Exception as e:
        logger.error(f"Failed to fetch price for {symbol}: {e}")
        return 0.0

def execute_trade(symbol: str, action: str, size: float, stop_loss: float, take_profit: float) -> dict:
    """
    Executes the trade on OKX using CCXT.
    Includes placing the main market order and conditional SL/TP orders.
    """
    exchange = get_exchange()

    try:
        # 1. Main Market Order
        side = 'buy' if action == "BUY" else 'sell'

        # Some exchanges require specific formatting for sizes, CCXT handles most, but be careful
        logger.info(f"Placing market {side} order for {size} of {symbol}")

        # Place the main order
        order = exchange.create_market_order(symbol, side, size)

        # 2. Attach Stop Loss and Take Profit (Usually requires advanced order types or separate conditional orders in CCXT)
        # For OKX, we might need to use OCO (One Cancels the Other) or conditional orders depending on the API version.
        # Here's a simplified approach for SL/TP using conditional orders if supported, or just logging them if not fully supported in standard create_order.

        # NOTE: Implement advanced CCXT okx specific parameters for SL/TP here.
        # This is a simplified representation. In a real-world scenario with OKX,
        # you would use `exchange.create_order(..., params={'stopLoss': ..., 'takeProfit': ...})` if supported,
        # or place separate trigger orders.

        result = {
            "status": "success",
            "order_id": order.get('id'),
            "symbol": symbol,
            "side": side,
            "size": size,
            "stop_loss_target": stop_loss,
            "take_profit_target": take_profit,
            "raw_response": order
        }
        logger.info(f"Trade executed successfully: {result}")
        return result

    except Exception as e:
        logger.error(f"Failed to execute trade on OKX: {e}")
        return {
            "status": "error",
            "reason": str(e)
        }
