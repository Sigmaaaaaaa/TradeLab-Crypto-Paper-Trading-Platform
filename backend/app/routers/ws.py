# backend/app/routers/ws.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.ws_manager import manager

router = APIRouter(tags=["websocket"])


@router.websocket("/ws/live")
async def websocket_live(websocket: WebSocket):
    """
    Frontend connects here to receive live price ticks.
    
    Messages sent to client:
    - { "type": "snapshot", "prices": { "BTCUSDT": 65000.1, ... } }
    - { "type": "tick", "symbol": "BTCUSDT", "price": 65012.5 }
    """
    await manager.connect(websocket)
    try:
        while True:
            # We keep the connection alive.
            # Frontend can send ping messages if desired; we just ignore them.
            data = await websocket.receive_text()
            # Optional: handle client messages here later if needed
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)