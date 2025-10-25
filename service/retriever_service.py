import httpx
from typing import List, Dict, Any, Optional



class RetrieverService:
    def __init__(self):
        self.endpoint_url = "http://default-url.com"

    def retrieve_data(self,query:str) -> List[dict]:

        return [
            {
                "content": "Databases are where we store data",
                "meta": {"source": "Sample source"}
            },
            {
                "content": "Photos are which catpure events",
                "meta": {"source": "Another source"}
            }
        ]

