"""Webhook receiver for marketing platform events."""

from datetime import datetime, timezone
from dataclasses import dataclass, field
import hashlib
import hmac


@dataclass
class WebhookEvent:
    platform: str
    event_type: str
    payload: dict
    received_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    verified: bool = False


class WebhookReceiver:
    def __init__(self):
        self._events: list[WebhookEvent] = []
        self._secrets = {
            "meta": "meta_webhook_secret_demo",
            "google": "google_webhook_secret_demo",
        }

    def verify_signature(
        self, platform: str, payload: str, signature: str
    ) -> bool:
        secret = self._secrets.get(platform, "")
        if not secret:
            return False
        expected = hmac.new(
            secret.encode(), payload.encode(), hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, signature)

    def process(
        self,
        platform: str,
        event_type: str,
        payload: dict,
        signature: str = "",
    ) -> WebhookEvent:
        verified = bool(signature)  # In demo, accept all
        event = WebhookEvent(
            platform=platform,
            event_type=event_type,
            payload=payload,
            verified=verified,
        )
        self._events.append(event)
        return event

    def get_events(
        self, platform: str = None, limit: int = 50
    ) -> list[dict]:
        filtered = self._events
        if platform:
            filtered = [e for e in filtered if e.platform == platform]
        return [
            {
                "platform": e.platform,
                "type": e.event_type,
                "payload": e.payload,
                "received_at": e.received_at,
                "verified": e.verified,
            }
            for e in filtered[-limit:]
        ]
