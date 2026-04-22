VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP"}

def validate_order(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float = None,
    stop_price: float = None,
) -> None:
    
    errors = []

    if not symbol or not symbol.strip():
        errors.append("Symbol cannot be empty (e.g. BTCUSDT).")

    if side.upper() not in VALID_SIDES:
        errors.append(f"Side '{side}' is invalid. Must be one of {VALID_SIDES}.")

    if order_type.upper() not in VALID_ORDER_TYPES:
        errors.append(f"Order type '{order_type}' is invalid. Must be one of {VALID_ORDER_TYPES}.")

    if quantity is None or quantity <= 0:
        errors.append("Quantity must be a positive number.")

    if order_type.upper() == "LIMIT":
        if price is None:
            errors.append("Price is required for LIMIT orders (--price).")
        elif price <= 0:
            errors.append("Price must be a positive number.")

    if order_type.upper() == "STOP":
        if price is None:
            errors.append("Price is required for STOP orders (--price).")
        elif price <= 0:
            errors.append("Price must be a positive number.")
        if stop_price is None:
            errors.append("Stop price is required for STOP orders (--stop-price).")
        elif stop_price <= 0:
            errors.append("Stop price must be a positive number.")

    if errors:
        raise ValueError("\n  ".join(errors))
