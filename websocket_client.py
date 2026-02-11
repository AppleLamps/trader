"""
WebSocket client for real-time Polymarket market data.

Replaces polling with push-based updates for ~100ms latency instead of 10-15s.

Subscribes to:
  - book: Full orderbook snapshots on every trade
  - price_change: Order placement/cancellation updates
  - best_bid_ask: BBO changes (requires custom_feature_enabled)
  - new_market: New market creation (auto-discover new arbs)
  - market_resolved: Market resolution (trigger position settlement)
  - last_trade_price: Trade execution events
"""

import json
import logging
import threading
import time
from typing import Callable, Optional

import websocket

log = logging.getLogger("polyarb.ws")


class PolyWebSocket:
    """
    WebSocket client for Polymarket CLOB market data.

    Provides real-time orderbook updates, new market alerts,
    and resolution notifications via callbacks.
    """

    def __init__(
        self,
        ws_url: str = "wss://ws-subscriptions-clob.polymarket.com/ws/market",
        on_book_update: Optional[Callable] = None,
        on_price_change: Optional[Callable] = None,
        on_best_bid_ask: Optional[Callable] = None,
        on_new_market: Optional[Callable] = None,
        on_market_resolved: Optional[Callable] = None,
        on_last_trade: Optional[Callable] = None,
    ):
        self.ws_url = ws_url
        self.ws: Optional[websocket.WebSocketApp] = None
        self._thread: Optional[threading.Thread] = None
        self._running = False
        self._subscribed_assets: set[str] = set()
        self._reconnect_delay = 1  # exponential backoff

        # Callbacks
        self.on_book_update = on_book_update
        self.on_price_change = on_price_change
        self.on_best_bid_ask = on_best_bid_ask
        self.on_new_market = on_new_market
        self.on_market_resolved = on_market_resolved
        self.on_last_trade = on_last_trade

    def connect(self, asset_ids: list[str] | None = None) -> None:
        """Start the WebSocket connection in a background thread."""
        if self._running:
            return

        self._running = True
        initial_assets = asset_ids or []
        self._subscribed_assets.update(initial_assets)

        self._thread = threading.Thread(
            target=self._run_forever,
            args=(initial_assets,),
            daemon=True,
        )
        self._thread.start()
        log.info("WebSocket connecting to %s with %d initial assets...",
                 self.ws_url, len(initial_assets))

    def _run_forever(self, initial_assets: list[str]) -> None:
        """Connection loop with auto-reconnect."""
        while self._running:
            try:
                self.ws = websocket.WebSocketApp(
                    self.ws_url,
                    on_open=lambda ws: self._on_open(ws, initial_assets),
                    on_message=self._on_message,
                    on_error=self._on_error,
                    on_close=self._on_close,
                )
                self.ws.run_forever(ping_interval=30, ping_timeout=10)
            except Exception as e:
                log.error("WebSocket error: %s", e)

            if self._running:
                log.info("WebSocket reconnecting in %ds...", self._reconnect_delay)
                time.sleep(self._reconnect_delay)
                self._reconnect_delay = min(self._reconnect_delay * 2, 30)

    def _on_open(self, ws, initial_assets: list[str]) -> None:
        """Subscribe to market channel on connection."""
        self._reconnect_delay = 1  # reset backoff

        # Subscribe message — market channel, no auth needed
        sub_msg = {
            "type": "MARKET",
            "assets_ids": initial_assets,
            "custom_feature_enabled": True,  # enables best_bid_ask, new_market, market_resolved
        }
        ws.send(json.dumps(sub_msg))
        log.info("WebSocket connected. Subscribed to %d assets with custom features enabled.",
                 len(initial_assets))

    def _on_message(self, ws, message: str) -> None:
        """Route incoming messages to the appropriate callback."""
        try:
            data = json.loads(message)
        except json.JSONDecodeError:
            log.debug("Non-JSON WS message: %s", message[:100])
            return

        # Handle array messages (some channels send arrays)
        if isinstance(data, list):
            for item in data:
                self._route_message(item)
        else:
            self._route_message(data)

    def _route_message(self, data: dict) -> None:
        """Dispatch a single message to the right callback."""
        event_type = data.get("event_type", "")

        try:
            if event_type == "book" and self.on_book_update:
                self.on_book_update(data)
            elif event_type == "price_change" and self.on_price_change:
                self.on_price_change(data)
            elif event_type == "best_bid_ask" and self.on_best_bid_ask:
                self.on_best_bid_ask(data)
            elif event_type == "new_market" and self.on_new_market:
                self.on_new_market(data)
            elif event_type == "market_resolved" and self.on_market_resolved:
                self.on_market_resolved(data)
            elif event_type == "last_trade_price" and self.on_last_trade:
                self.on_last_trade(data)
        except Exception as e:
            log.error("Error in WS callback for %s: %s", event_type, e, exc_info=True)

    def _on_error(self, ws, error) -> None:
        log.error("WebSocket error: %s", error)

    def _on_close(self, ws, close_status_code, close_msg) -> None:
        log.info("WebSocket closed: code=%s msg=%s", close_status_code, close_msg)

    def subscribe(self, asset_ids: list[str]) -> None:
        """Subscribe to additional asset IDs on an active connection."""
        if not asset_ids:
            return

        new_ids = [aid for aid in asset_ids if aid not in self._subscribed_assets]
        if not new_ids:
            return

        self._subscribed_assets.update(new_ids)

        if self.ws and self.ws.sock and self.ws.sock.connected:
            msg = {
                "assets_ids": new_ids,
                "operation": "subscribe",
                "custom_feature_enabled": True,
            }
            try:
                self.ws.send(json.dumps(msg))
                log.info("Subscribed to %d additional assets (total: %d)",
                         len(new_ids), len(self._subscribed_assets))
            except Exception as e:
                log.error("Failed to subscribe to new assets: %s", e)

    def unsubscribe(self, asset_ids: list[str]) -> None:
        """Unsubscribe from asset IDs."""
        if not asset_ids:
            return

        self._subscribed_assets -= set(asset_ids)

        if self.ws and self.ws.sock and self.ws.sock.connected:
            msg = {
                "assets_ids": asset_ids,
                "operation": "unsubscribe",
            }
            try:
                self.ws.send(json.dumps(msg))
                log.debug("Unsubscribed from %d assets", len(asset_ids))
            except Exception:
                pass

    def disconnect(self) -> None:
        """Stop the WebSocket connection."""
        self._running = False
        if self.ws:
            try:
                self.ws.close()
            except Exception:
                pass
        if self._thread:
            self._thread.join(timeout=5)
        log.info("WebSocket disconnected.")

    @property
    def is_connected(self) -> bool:
        return (
            self.ws is not None
            and self.ws.sock is not None
            and self.ws.sock.connected
        )

    @property
    def subscribed_count(self) -> int:
        return len(self._subscribed_assets)
