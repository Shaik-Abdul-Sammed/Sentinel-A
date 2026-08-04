from typing import Any, Dict, Set

from fastapi import WebSocket


class WSManager:
    def __init__(self) -> None:
        self.active: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active.add(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        if websocket in self.active:
            self.active.remove(websocket)

    async def broadcast(self, message: Dict[str, Any]) -> None:
        stale: Set[WebSocket] = set()
        for ws in self.active:
            try:
                await ws.send_json(message)
            except Exception:
                stale.add(ws)
        for ws in stale:
            self.disconnect(ws)


ws_manager = WSManager()
