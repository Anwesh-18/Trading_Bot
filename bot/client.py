import os
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from dotenv import load_dotenv
from bot.logging_config import setup_logger

load_dotenv()
logger = setup_logger()

FUTURES_TESTNET_URL = "https://testnet.binancefuture.com/fapi"


class BinanceClient:

    def __init__(self):
        api_key = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_API_SECRET")

        if not api_key or not api_secret:
            raise EnvironmentError(
                "BINANCE_API_KEY and BINANCE_API_SECRET must be set in your .env file."
            )

        self.client = Client(api_key, api_secret, testnet=True)
        self.client.FUTURES_URL = FUTURES_TESTNET_URL
        logger.info("BinanceClient initialised — connected to Futures Testnet")

    def place_order(self, **kwargs) -> dict:
        logger.info(f"REQUEST  → futures_create_order | params={kwargs}")
        try:
            response = self.client.futures_create_order(**kwargs)
            logger.info(f"RESPONSE ← {response}")
            return response
        except BinanceAPIException as e:
            logger.error(f"BinanceAPIException | status={e.status_code} | msg={e.message}")
            raise
        except BinanceRequestException as e:
            logger.error(f"BinanceRequestException | {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during order placement | {e}")
            raise
