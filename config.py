"""
Configuration management — loads settings from .env and validates them.
"""

import os
import sys
from dataclasses import dataclass
try:
    from dotenv import load_dotenv
except ModuleNotFoundError:  # pragma: no cover - keeps local tooling usable without optional dependency
    def load_dotenv(*_args, **_kwargs):
        return False


@dataclass
class Config:
    # Polymarket connection
    private_key: str
    funder_address: str
    clob_host: str
    chain_id: int

    # Builder program (optional but recommended for fee reductions)
    builder_api_key: str
    builder_secret: str
    builder_passphrase: str

    # Strategy — fees are now fetched per-market from the API
    min_profit_margin: float
    min_roi: float
    min_fill_confidence: float
    max_position_size: float
    max_total_exposure: float
    max_trades_per_cycle: int
    scan_interval: int
    min_book_depth: float
    dry_run: bool
    log_level: str

    # Sanity filters (prevent bogus arb signals)
    min_cost_threshold: float   # Skip if total cost < this (stale/abandoned orders)
    max_profit_per_share: float  # Skip if profit/share > this (too good to be true)
    min_arb_value: float         # Skip if estimated profit < this $ amount
    min_market_liquidity: float  # Skip Gamma markets with liquidity below this

    # WebSocket
    ws_enabled: bool
    ws_host: str

    # Heartbeat (dead man's switch — auto-cancels all orders if bot crashes)
    heartbeat_enabled: bool
    heartbeat_interval: int  # seconds

    # Execution
    use_fok_orders: bool          # Fill-Or-Kill for arb legs
    use_batch_orders: bool        # Batch submit all legs at once
    gtd_expiry_seconds: int       # GTD order expiry (0 = use GTC)
    require_full_match: bool      # Require every leg to be immediately matched
    failure_cooldown_seconds: int # Back off failed markets to avoid churn

    # Pre-flight checks
    balance_check_enabled: bool

    @property
    def has_builder_config(self) -> bool:
        return bool(self.builder_api_key and self.builder_secret and self.builder_passphrase)


def load_config() -> Config:
    """Load configuration from .env file and environment variables."""
    load_dotenv()

    private_key = os.getenv("PRIVATE_KEY", "")
    funder_address = os.getenv("FUNDER_ADDRESS", "")

    if not private_key or private_key == "0xYOUR_PRIVATE_KEY_HERE":
        print("ERROR: Set PRIVATE_KEY in your .env file.")
        sys.exit(1)
    if not funder_address or funder_address == "0xYOUR_FUNDER_ADDRESS_HERE":
        print("ERROR: Set FUNDER_ADDRESS in your .env file.")
        sys.exit(1)

    return Config(
        private_key=private_key,
        funder_address=funder_address,
        clob_host=os.getenv("CLOB_HOST", "https://clob.polymarket.com"),
        chain_id=int(os.getenv("CHAIN_ID", "137")),

        # Builder config
        builder_api_key=os.getenv("BUILDER_API_KEY", ""),
        builder_secret=os.getenv("BUILDER_SECRET", ""),
        builder_passphrase=os.getenv("BUILDER_PASSPHRASE", ""),

        # Strategy — no more hardcoded taker_fee_rate; fees are fetched per-market
        min_profit_margin=float(os.getenv("MIN_PROFIT_MARGIN", "0.005")),
        min_roi=float(os.getenv("MIN_ROI", "0.004")),
        min_fill_confidence=float(os.getenv("MIN_FILL_CONFIDENCE", "0.35")),
        max_position_size=float(os.getenv("MAX_POSITION_SIZE", "50.0")),
        max_total_exposure=float(os.getenv("MAX_TOTAL_EXPOSURE", "500.0")),
        max_trades_per_cycle=int(os.getenv("MAX_TRADES_PER_CYCLE", "3")),
        scan_interval=int(os.getenv("SCAN_INTERVAL", "10")),
        min_book_depth=float(os.getenv("MIN_BOOK_DEPTH", "100")),
        dry_run=os.getenv("DRY_RUN", "true").lower() in ("true", "1", "yes"),
        log_level=os.getenv("LOG_LEVEL", "INFO").upper(),

        # Sanity filters
        min_cost_threshold=float(os.getenv("MIN_COST_THRESHOLD", "0.90")),
        max_profit_per_share=float(os.getenv("MAX_PROFIT_PER_SHARE", "0.05")),
        min_arb_value=float(os.getenv("MIN_ARB_VALUE", "0.50")),
        min_market_liquidity=float(os.getenv("MIN_MARKET_LIQUIDITY", "1000")),

        # WebSocket
        ws_enabled=os.getenv("WS_ENABLED", "true").lower() in ("true", "1", "yes"),
        ws_host=os.getenv("WS_HOST", "wss://ws-subscriptions-clob.polymarket.com/ws/market"),

        # Heartbeat
        heartbeat_enabled=os.getenv("HEARTBEAT_ENABLED", "true").lower() in ("true", "1", "yes"),
        heartbeat_interval=int(os.getenv("HEARTBEAT_INTERVAL", "5")),

        # Execution
        use_fok_orders=os.getenv("USE_FOK_ORDERS", "true").lower() in ("true", "1", "yes"),
        use_batch_orders=os.getenv("USE_BATCH_ORDERS", "true").lower() in ("true", "1", "yes"),
        gtd_expiry_seconds=int(os.getenv("GTD_EXPIRY_SECONDS", "30")),
        require_full_match=os.getenv("REQUIRE_FULL_MATCH", "true").lower() in ("true", "1", "yes"),
        failure_cooldown_seconds=int(os.getenv("FAILURE_COOLDOWN_SECONDS", "20")),

        # Pre-flight
        balance_check_enabled=os.getenv("BALANCE_CHECK_ENABLED", "true").lower() in ("true", "1", "yes"),
    )
