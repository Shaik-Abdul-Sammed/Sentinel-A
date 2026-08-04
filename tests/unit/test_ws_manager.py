import pytest

from backend.app.services.ws_manager import WSManager


class DummyWebSocket:
    def __init__(self):
        self.sent = []

    async def accept(self):
        return None

    async def send_json(self, message):
        self.sent.append(message)


@pytest.mark.asyncio
async def test_ws_manager_broadcasts_to_connected_clients():
    manager = WSManager()
    ws = DummyWebSocket()
    await manager.connect(ws)
    await manager.broadcast({"type": "hello"})
    assert ws.sent == [{"type": "hello"}]
