"""Multi-account/client management."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import uuid


@dataclass
class ClientAccount:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    meta_account_id: str = ""
    google_account_id: str = ""
    ga4_property_id: str = ""
    status: str = "active"
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


class AccountManager:
    def __init__(self):
        self._accounts: dict[str, ClientAccount] = {}
        self._seed_demo()

    def _seed_demo(self):
        demos = [
            ClientAccount(
                name="Smith & Associates Law Firm",
                meta_account_id="act_001",
                google_account_id="gact_001",
                ga4_property_id="prop_001",
            ),
            ClientAccount(
                name="Johnson Legal Group",
                meta_account_id="act_002",
                google_account_id="gact_002",
                ga4_property_id="prop_002",
            ),
            ClientAccount(
                name="Martinez & Partners",
                meta_account_id="act_003",
                google_account_id="gact_003",
                ga4_property_id="prop_003",
            ),
        ]
        for a in demos:
            self._accounts[a.id] = a

    def list_accounts(self) -> list[dict]:
        return [
            {
                "id": a.id,
                "name": a.name,
                "status": a.status,
                "platforms": {
                    "meta": bool(a.meta_account_id),
                    "google": bool(a.google_account_id),
                    "ga4": bool(a.ga4_property_id),
                },
            }
            for a in self._accounts.values()
        ]

    def get_account(self, account_id: str) -> dict | None:
        a = self._accounts.get(account_id)
        if not a:
            return None
        return {
            "id": a.id,
            "name": a.name,
            "meta_account_id": a.meta_account_id,
            "google_account_id": a.google_account_id,
            "ga4_property_id": a.ga4_property_id,
            "status": a.status,
        }

    def create_account(
        self,
        name: str,
        meta_id: str = "",
        google_id: str = "",
        ga4_id: str = "",
    ) -> dict:
        a = ClientAccount(
            name=name,
            meta_account_id=meta_id,
            google_account_id=google_id,
            ga4_property_id=ga4_id,
        )
        self._accounts[a.id] = a
        return self.get_account(a.id)
