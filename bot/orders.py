from bot.client import BinanceClient
from bot.validators import validate_order
from bot.logging_config import setup_logger

logger = setup_logger()


class OrderManager:

    def __init__(self):
        self.client = BinanceClient()

    def place_market_order(self, symbol: str, side: str, quantity: float) -> dict:
        validate_order(symbol, side, "MARKET", quantity)
        logger.info(f"Placing MARKET order | symbol={symbol} side={side} qty={quantity}")
        return self.client.place_order(
            symbol=symbol.upper(),
            side=side.upper(),
            type="MARKET",
            quantity=quantity,
        )

    def place_limit_order(
        self, symbol: str, side: str, quantity: float, price: float
    ) -> dict:
        validate_order(symbol, side, "LIMIT", quantity, price=price)
        logger.info(
            f"Placing LIMIT order | symbol={symbol} side={side} qty={quantity} price={price}"
        )
        return self.client.place_order(
            symbol=symbol.upper(),
            side=side.upper(),
            type="LIMIT",
            quantity=quantity,
            price=price,
            timeInForce="GTC",
        )
    
    def place_stop_limit_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
        price: float,
        stop_price: float,
    ) -> dict:
        validate_order(symbol, side, "STOP", quantity, price=price, stop_price=stop_price)
        logger.info(
            f"Placing STOP order | symbol={symbol} side={side} "
            f"qty={quantity} price={price} stopPrice={stop_price}"
        )
        return self.client.place_order(
            symbol=symbol.upper(),
            side=side.upper(),
            type="STOP",
            quantity=quantity,
            price=price,
            stopPrice=stop_price,
            timeInForce="GTC",
        )
