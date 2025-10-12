import httpx
from typing import List, Dict, Any, Optional

from dto.RetreverResponseDto import Fact


class RetrieverService:
    def __init__(self, endpoint_url: str):
        self.endpoint_url = endpoint_url

    def retrieve(self, query: str, domain_id: str, user_id: str = "user", channel_id: str = "default", conversation_id: str = "conv") -> List[Fact]:
        client_info = {
            "domainId": domain_id,
            "channelId": channel_id,
            "conversationId": conversation_id,
            "user": {"id": user_id}
        }
        payload = {
            "client": client_info,
            "query": query,
            "appContext": [domain_id],
            "context": None,
            "experiments": {}
        }
        try:
            response = httpx.post(f"{self.endpoint_url}/retrieve-facts", json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data.get("status") == "SUCCESS":
                facts = [Fact(fact["content"], fact.get("meta", {})) for fact in data.get("facts", [])]
                return facts
            else:
                # Log or handle errors as needed
                return []
        except Exception as e:
            # Log or handle errors as needed
            print("exception occurred while retrieving ", e)
            return []

