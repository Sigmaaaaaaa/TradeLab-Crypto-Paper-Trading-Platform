# backend/app/services/ws_manager.py

import asyncio
import json
from typing import Dict, Set, List
from fastapi import WebSocket

from app.config import BINANCE_WS_URL, ALLOWED_SYMBOLS


class ConnectionManager:
    """
    Manages frontend WebSocket connections and a single background
    task that listens to Binance and broadcasts ticks to all clients.
    """

    def __init__(self):
        # All active frontend WebSocket connections
        self.active_connections: Set[WebSocket] = set()
        
        # Latest prices cache { "BTCUSDT": 65000.12, ... }
        self.latest_prices: Dict[str, float] = {}
        
        # Background task handle
        self.binance_task = None
        self._running = False

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        
        # Send the current price cache immediately so the client has data
        if self.latest_prices:
            await websocket.send_json({
                "type": "snapshot",
                "prices": self.latest_prices
            })

    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)

    async def broadcast(self, message: dict):
        """Send a message to every connected frontend client."""
        if not self.active_connections:
            return
        
        dead = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                dead.append(connection)
        
        for conn in dead:
            self.disconnect(conn)

    async def _binance_listener(self):
        """
        Connects to Binance combined stream and pushes ticks.
        We subscribe to all ALLOWED_SYMBOLS in one connection.
        """
        import websockets
        
        # Build combined stream URL
        # e.g. btcusdt@trade/ethusdt@trade/...
        streams = "/".join([f"{s.lower()}@trade" for s in ALLOWED_SYMBOLS])
        url = f"{BINANCE_WS_URL}/{streams}"
        
        print(f"[ws_manager] Connecting to Binance: {url}")
        
        while self._running:
            try:
                async with websockets.connect(url, ping_interval=20) as ws:
                    print("[ws_manager] Connected to Binance WebSocket")
                    async for raw in ws:
                        if not self._running:
                            break
                        
                        data = json.loads(raw)
                        
                        # Combined stream wraps the data
                        if "data" in data:
                            trade = data["data"]
                        else:
                            trade = data
                        
                        symbol = trade.get("s")          # e.g. "BTCUSDT"
                        price = float(trade.get("p", 0)) # last trade price
                        
                        if symbol and price > 0:
                            self.latest_prices[symbol] = price
                            
                            # Broadcast to all frontend clients
                            await self.broadcast({
                                "type": "tick",
                                "symbol": symbol,
                                "price": price
                            })
            
            except Exception as e:
                print(f"[ws_manager] Binance connection error: {e}")
                if self._running:
                    print("[ws_manager] Reconnecting in 5 seconds...")
                    await asyncio.sleep(5)

    def start_binance_listener(self):
        """Start the background Binance listener (call once at startup)."""
        if self.binance_task is None:
            self._running = True
            self.binance_task = asyncio.create_task(self._binance_listener())
            print("[ws_manager] Binance listener started")

    def stop_binance_listener(self):
        """Stop the background task."""
        self._running = False
        if self.binance_task:
            self.binance_task.cancel()
            self.binance_task = None


# Global singleton instance
manager = ConnectionManager()