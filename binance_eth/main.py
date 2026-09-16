"""Print live ETH/USDT trades from Binance's public WebSocket stream."""

import asyncio
import json
import logging
from datetime import datetime, timezone

from websockets.asyncio.client import connect
from websockets.exceptions import ConnectionClosed


STREAM_URL = "wss://stream.binance.com:9443/ws/ethusdt@trade"
RECONNECT_DELAY_SECONDS = 5


def utc_datetime(timestamp_ms: int) -> str:
    """Convert a Unix timestamp in milliseconds to a readable UTC datetime."""
    return datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S.%f"
    )[:-3]


def print_trade(message: str) -> None:
    """Parse and print one Binance trade message."""
    trade = json.loads(message)

    symbol = trade["s"]
    event_time = utc_datetime(trade["E"])
    trade_time = utc_datetime(trade["T"])
    price = float(trade["p"])
    quantity = float(trade["q"])

    print(
        f"{symbol} | Price: {price} | Quantity: {quantity} | "
        f"Event Time: {event_time} UTC | Trade Time: {trade_time} UTC",
        flush=True,
    )


async def stream_trades() -> None:
    """Connect to Binance and reconnect whenever the connection is lost."""
    while True:
        try:
            logging.info("Connecting to %s", STREAM_URL)
            async with connect(STREAM_URL) as websocket:
                logging.info("Connected; streaming ETHUSDT trades")
                async for message in websocket:
                    try:
                        print_trade(message)
                    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
                        logging.exception("Could not parse trade message")
        except (ConnectionClosed, OSError) as error:
            logging.warning(
                "WebSocket disconnected (%s). Reconnecting in %s seconds...",
                error,
                RECONNECT_DELAY_SECONDS,
            )
            await asyncio.sleep(RECONNECT_DELAY_SECONDS)


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    try:
        asyncio.run(stream_trades())
    except KeyboardInterrupt:
        logging.info("Stopped by user")


if __name__ == "__main__":
    main()
