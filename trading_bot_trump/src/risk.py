import time
from typing import Tuple, Dict
from src.config import MAX_CAPITAL_PER_ORDER_USDT, COOLDOWN_SECONDS
from src.database import logger

# In-memory dictionary for cooldown management.
# Key: symbol (e.g., 'BTC/USDT'), Value: float (timestamp of last trade)
_last_trade_times: Dict[str, float] = {}

def check_cooldown(symbol: str) -> bool:
    """
    Checks if a trade for the given symbol is allowed based on the cooldown period.
    Returns True if allowed, False if in cooldown.
    """
    current_time = time.time()
    last_trade_time = _last_trade_times.get(symbol, 0.0)

    if current_time - last_trade_time < COOLDOWN_SECONDS:
        logger.warning(f"Cooldown active for {symbol}. Ignoring trade signal.")
        return False

    return True

def update_cooldown(symbol: str):
    """
    Updates the last trade time for a symbol.
    """
    _last_trade_times[symbol] = time.time()

def calculate_position_size(symbol: str, current_price: float) -> float:
    """
    Calculates the size of the position based on the fixed max capital.
    """
    if current_price <= 0:
        logger.error(f"Invalid current price for {symbol}: {current_price}")
        return 0.0

    # Capital limit per order (e.g., 50 USDT)
    size = MAX_CAPITAL_PER_ORDER_USDT / current_price
    logger.info(f"Calculated position size for {symbol} at {current_price}: {size}")
    return size

def calculate_sl_tp(action: str, current_price: float, sl_pct: float = 0.02, tp_pct: float = 0.05) -> Tuple[float, float]:
    """
    Calculates Stop Loss and Take Profit prices based on standard percentages.
    Defaults: 2% SL, 5% TP
    """
    if action == "BUY":
        stop_loss = current_price * (1 - sl_pct)
        take_profit = current_price * (1 + tp_pct)
    elif action == "SELL":
        stop_loss = current_price * (1 + sl_pct)
        take_profit = current_price * (1 - tp_pct)
    else:
        raise ValueError(f"Invalid action: {action}")

    logger.info(f"Calculated SL/TP for {action} at {current_price}: SL={stop_loss}, TP={take_profit}")
    return stop_loss, take_profit

def validate_trade_risk(symbol: str, action: str, current_price: float) -> dict:
    """
    Main risk validation function.
    Returns a dict with validation status and calculated parameters.
    """
    if not check_cooldown(symbol):
        return {"approved": False, "reason": "COOLDOWN"}

    size = calculate_position_size(symbol, current_price)
    if size <= 0:
        return {"approved": False, "reason": "INVALID_SIZE"}

    stop_loss, take_profit = calculate_sl_tp(action, current_price)

    return {
        "approved": True,
        "size": size,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "max_capital_usdt": MAX_CAPITAL_PER_ORDER_USDT
    }
