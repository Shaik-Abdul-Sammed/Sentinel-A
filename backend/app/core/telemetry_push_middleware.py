from __future__ import annotations

from datetime import datetime, timezone
from urllib.parse import parse_qs

from app.services.telemetry_engine import TelemetryEvent, engine
from app.services.ws_manager import ws_manager


class TelemetryPushMiddleware:
    """Pushes live-login auth events into Sentinel-A telemetry without breaking the response flow."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope.get("type") != "http" or scope.get("path") != "/auth/live-login" or scope.get("method") != "POST":
            await self.app(scope, receive, send)
            return

        captured_body = bytearray()
        response_status = {"value": 200}

        async def receive_wrapper():
            message = await receive()
            if message.get("type") == "http.request":
                captured_body.extend(message.get("body", b""))
            return message

        async def send_wrapper(message):
            if message.get("type") == "http.response.start":
                response_status["value"] = int(message.get("status", 200))
            await send(message)

        await self.app(scope, receive_wrapper, send_wrapper)

        try:
            form = parse_qs(captured_body.decode("utf-8"))
            username = (form.get("username") or ["unknown"])[0]
            status = "SUCCESS" if response_status["value"] < 400 else "FAILED"
            client = scope.get("client")
            client_ip = client[0] if client else "0.0.0.0"

            event = TelemetryEvent(
                source="live-auth-middleware",
                event_type="AUTH",
                actor_id=username,
                ip=client_ip,
                endpoint=scope.get("path", "/auth/live-login"),
                status=status,
                payload={
                    "action_count": 1,
                    "hour_of_day": datetime.now(timezone.utc).hour,
                    "data_volume_mb": 0,
                    "user_agent": next((value.decode("latin-1") for key, value in scope.get("headers", []) if key == b"user-agent"), "unknown"),
                    "status_code": response_status["value"],
                },
                timestamp=datetime.now(timezone.utc).isoformat(),
            )

            result = await engine.ingest(event)
            await ws_manager.broadcast(
                {
                    "type": "telemetry.update",
                    "status": engine.get_status(),
                    "latest_alert": result.get("alert"),
                    "latest_timeline": engine.get_timeline(1),
                }
            )
        except Exception:
            # Middleware telemetry must never break authentication flow.
            pass
