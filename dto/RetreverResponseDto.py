from typing import List, Dict


class Fact:
    def __init__(self, content: str, meta: Dict[str, str]):
        self.content = content
        self.meta = meta

class RetrieverError:
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message

class RetrieverResponse:
    def __init__(self, status: str, facts: List[Fact], errors: List[RetrieverError]):
        self.status = status
        self.facts = facts
        self.errors = errors
