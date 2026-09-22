# backend/app/services/ws_manager.py

import asyncio
import json
from typing import Dict, Set
from fastapi import WebSocket

from app.config import COINBASE_PRODUCTS, COINBASE_WS_URL


class ConnectionManager:
    """
    Manages frontend WebSocket connections and a single background
    task that listens to Coinbase and broadcasts ticks to all clients.
    """

    def __init__(self):
        # All active frontend WebSocket connections
        self.active_connections: Set[WebSocket] = set()
        
        # Latest prices cache { "BTCUSDT": 65000.12, ... }
        self.latest_prices: Dict[str, float] = {}
        
        # Background task handle
        self.market_data_task = None
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

    async def _coinbase_listener(self):
        """
        Connects to Coinbase's public ticker channel and pushes ticks.
        Coinbase product IDs are translated back to the application's symbols.
        """
        import websockets
        
        while self._running:
            try:
                async with websockets.connect(COINBASE_WS_URL, ping_interval=20) as ws:
                    await ws.send(json.dumps({
                        "type": "subscribe",
                        "product_ids": list(COINBASE_PRODUCTS.values()),
                        "channels": ["ticker"],
                    }))
                    print("[ws_manager] Connected to Coinbase WebSocket")

                    product_to_symbol = {
                        product: symbol
                        for symbol, product in COINBASE_PRODUCTS.items()
                    }
                    async for raw in ws:
                        if not self._running:
                            break
                        
                        data = json.loads(raw)

                        if data.get("type") != "ticker":
                            continue

                        symbol = product_to_symbol.get(data.get("product_id"))
                        price = float(data.get("price", 0))
                        
                        if symbol and price > 0:
                            self.latest_prices[symbol] = price
                            
                            # Broadcast to all frontend clients
                            await self.broadcast({
                                "type": "tick",
                                "symbol": symbol,
                                "price": price
                            })
            
            except Exception as e:
                print(f"[ws_manager] Coinbase connection error: {e}")
                if self._running:
                    print("[ws_manager] Reconnecting in 5 seconds...")
                    await asyncio.sleep(5)

    def start_market_data_listener(self):
        """Start the Coinbase listener (call once at startup)."""
        if self.market_data_task is None:
            self._running = True
            self.market_data_task = asyncio.create_task(self._coinbase_listener())
            print("[ws_manager] Coinbase listener started")

    def stop_market_data_listener(self):
        """Stop the background task."""
        self._running = False
        if self.market_data_task:
            self.market_data_task.cancel()
            self.market_data_task = None


# Global singleton instance
manager = ConnectionManager()