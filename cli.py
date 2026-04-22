import argparse
import sys
from binance.exceptions import BinanceAPIException, BinanceRequestException
from bot.orders import OrderManager
from bot.logging_config import setup_logger

logger = setup_logger()

def print_request_summary(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float = None,
    stop_price: float = None,
) -> None:
    print("\n┌─────────────────────────────────┐")
    print("│       Order Request Summary      │")
    print("├─────────────────────────────────┤")
    print(f"│  Symbol     : {symbol.upper():<19}│")
    print(f"│  Side       : {side.upper():<19}│")
    print(f"│  Type       : {order_type.upper():<19}│")
    print(f"│  Quantity   : {str(quantity):<19}│")
    if price is not None:
        print(f"│  Price      : {str(price):<19}│")
    if stop_price is not None:
        print(f"│  Stop Price : {str(stop_price):<19}│")
    print("└─────────────────────────────────┘\n")


def print_order_response(response: dict) -> None:
    print("┌─────────────────────────────────┐")
    print("│        Order Response            │")
    print("├─────────────────────────────────┤")
    print(f"│  Order ID     : {str(response.get('orderId', 'N/A')):<17}│")
    print(f"│  Status       : {str(response.get('status', 'N/A')):<17}│")
    print(f"│  Executed Qty : {str(response.get('executedQty', 'N/A')):<17}│")
    print(f"│  Avg Price    : {str(response.get('avgPrice', 'N/A')):<17}│")
    print(f"│  Symbol       : {str(response.get('symbol', 'N/A')):<17}│")
    print("└─────────────────────────────────┘")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--symbol",     required=True,  help="Trading pair symbol (e.g. BTCUSDT)")
    parser.add_argument("--side",       required=True,  choices=["BUY", "SELL"], help="Order side")
    parser.add_argument(
        "--type", required=True,
        choices=["MARKET", "LIMIT", "STOP"],
        dest="order_type",
        help="Order type",
    )
    parser.add_argument("--quantity",   required=True,  type=float, help="Order quantity")
    parser.add_argument("--price",      required=False, type=float, default=None,
                        help="Limit / stop-limit price (required for LIMIT and STOP)")
    parser.add_argument("--stop-price", required=False, type=float, default=None,
                        dest="stop_price",
                        help="Trigger price for STOP orders")
    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()

    print_request_summary(
        args.symbol, args.side, args.order_type,
        args.quantity, args.price, args.stop_price,
    )

    try:
        manager = OrderManager()

        if args.order_type == "MARKET":
            response = manager.place_market_order(args.symbol, args.side, args.quantity)

        elif args.order_type == "LIMIT":
            if args.price is None:
                print("--price is required for LIMIT orders.")
                sys.exit(1)
            response = manager.place_limit_order(
                args.symbol, args.side, args.quantity, args.price
            )

        elif args.order_type == "STOP":
            if args.price is None or args.stop_price is None:
                print("Both --price and --stop-price are required for STOP orders.")
                sys.exit(1)
            response = manager.place_stop_limit_order(
                args.symbol, args.side, args.quantity, args.price, args.stop_price
            )

        print_order_response(response)
        print("\n Order placed successfully!\n")
        logger.info("Order placed successfully")

    except ValueError as e:
        print(f"\n Validation Error:\n  {e}\n")
        logger.error(f"Validation error: {e}")
        sys.exit(1)

    except BinanceAPIException as e:
        print(f"\n Binance API Error [{e.status_code}]: {e.message}\n")
        logger.error(f"BinanceAPIException: {e.status_code} - {e.message}")
        sys.exit(1)

    except BinanceRequestException as e:
        print(f"\n Network / Request Error: {e}\n")
        logger.error(f"BinanceRequestException: {e}")
        sys.exit(1)

    except EnvironmentError as e:
        print(f"\n Environment Error: {e}\n")
        logger.error(f"EnvironmentError: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"\n Unexpected Error: {e}\n")
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
