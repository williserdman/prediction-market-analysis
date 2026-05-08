from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from dateutil.parser import isoparse


def parse_datetime(val: str) -> datetime:
    return isoparse(val)


@dataclass
class Trade:
    trade_id: str
    ticker: str
    count: int
    yes_price: int  # Stored as cents
    no_price: int  # Stored as cents
    taker_side: str
    created_time: datetime

    @classmethod
    def from_dict(cls, data: dict) -> "Trade":
        def parse_dollars_to_cents(val: Optional[str]) -> int:
            """Converts string dollar values like '0.5600' to integer cents (56)."""
            if not val:
                return 0
            return int(float(val) * 100)

        def parse_float_string_to_int(val: Optional[str]) -> int:
            """Converts string float values like '10.00' to integers (10)."""
            if not val:
                return 0
            return int(float(val))

        return cls(
            trade_id=data["trade_id"],
            ticker=data["ticker"],
            # Map the exact keys from the JSON and convert to standard ints
            count=parse_float_string_to_int(data.get("count_fp")),
            yes_price=parse_dollars_to_cents(data.get("yes_price_dollars")),
            no_price=parse_dollars_to_cents(data.get("no_price_dollars")),
            taker_side=data.get("taker_side", ""),
            created_time=parse_datetime(data["created_time"]),
        )


@dataclass
class Market:
    ticker: str
    event_ticker: str
    market_type: str
    title: str
    yes_sub_title: str
    no_sub_title: str
    status: str
    yes_bid: Optional[int]  # Stored as cents
    yes_ask: Optional[int]  # Stored as cents
    no_bid: Optional[int]  # Stored as cents
    no_ask: Optional[int]  # Stored as cents
    last_price: Optional[int]  # Stored as cents
    volume: int
    volume_24h: int
    open_interest: int
    result: str
    created_time: Optional[datetime]
    open_time: Optional[datetime]
    close_time: Optional[datetime]

    @classmethod
    def from_dict(cls, data: dict) -> "Market":
        def parse_time(val: Optional[str]) -> Optional[datetime]:
            if not val:
                return None
            return parse_datetime(val)

        def parse_dollars_to_cents(val: Optional[str]) -> Optional[int]:
            """Converts string dollar values like '0.5600' to integer cents (56)."""
            if not val:
                return None
            return int(float(val) * 100)

        def parse_float_string_to_int(val: Optional[str]) -> int:
            """Converts string float values like '10.00' to integers (10)."""
            if not val:
                return 0
            return int(float(val))

        return cls(
            ticker=data["ticker"],
            event_ticker=data["event_ticker"],
            market_type=data.get("market_type", "binary"),
            title=data.get("title", ""),
            yes_sub_title=data.get("yes_sub_title", ""),
            no_sub_title=data.get("no_sub_title", ""),
            status=data["status"],
            # Map to the exact keys in the JSON and convert to cents
            yes_bid=parse_dollars_to_cents(data.get("yes_bid_dollars")),
            yes_ask=parse_dollars_to_cents(data.get("yes_ask_dollars")),
            no_bid=parse_dollars_to_cents(data.get("no_bid_dollars")),
            no_ask=parse_dollars_to_cents(data.get("no_ask_dollars")),
            last_price=parse_dollars_to_cents(data.get("last_price_dollars")),
            # Map to the _fp (floating point) keys and convert to ints
            volume=parse_float_string_to_int(data.get("volume_fp")),
            volume_24h=parse_float_string_to_int(data.get("volume_24h_fp")),
            open_interest=parse_float_string_to_int(data.get("open_interest_fp")),
            result=data.get("result", ""),
            created_time=parse_time(data.get("created_time")),
            open_time=parse_time(data.get("open_time")),
            close_time=parse_time(data.get("close_time")),
        )


@dataclass
class Candle:
    end_period_ts: int
    # Price OHLC (Stored as cents)
    price_open: int
    price_high: int
    price_low: int
    price_close: int
    price_mean: int

    # Yes Bid OHLC (Stored as cents)
    yes_bid_open: int
    yes_bid_high: int
    yes_bid_low: int
    yes_bid_close: int

    # Yes Ask OHLC (Stored as cents)
    yes_ask_open: int
    yes_ask_high: int
    yes_ask_low: int
    yes_ask_close: int

    # Metrics
    volume: int
    open_interest: int

    @classmethod
    def from_dict(cls, data: dict) -> "Candle":
        def to_cents(val: Optional[str]) -> int:
            """Helper to convert '$0.5600' string to 56 integer cents."""
            if not val:
                return 0
            return int(float(val) * 100)

        def to_int(val: Optional[str]) -> int:
            """Helper to convert '10.00' string to 10 integer."""
            if not val:
                return 0
            return int(float(val))

        # Extract nested dictionaries
        price = data.get("price", {})
        y_bid = data.get("yes_bid", {})
        y_ask = data.get("yes_ask", {})

        return cls(
            end_period_ts=data.get("end_period_ts", 0),
            # Price mapping
            price_open=to_cents(price.get("open")),
            price_high=to_cents(price.get("high")),
            price_low=to_cents(price.get("low")),
            price_close=to_cents(price.get("close")),
            price_mean=to_cents(price.get("mean")),
            # Yes Bid mapping
            yes_bid_open=to_cents(y_bid.get("open")),
            yes_bid_high=to_cents(y_bid.get("high")),
            yes_bid_low=to_cents(y_bid.get("low")),
            yes_bid_close=to_cents(y_bid.get("close")),
            # Yes Ask mapping
            yes_ask_open=to_cents(y_ask.get("open")),
            yes_ask_high=to_cents(y_ask.get("high")),
            yes_ask_low=to_cents(y_ask.get("low")),
            yes_ask_close=to_cents(y_ask.get("close")),
            # Totals
            volume=to_int(data.get("volume")),
            open_interest=to_int(data.get("open_interest")),
        )
