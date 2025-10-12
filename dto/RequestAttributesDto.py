from dataclasses import field
from typing import Optional, Dict, Any

from pydantic.dataclasses import dataclass


@dataclass
class Entry:
    ref: Optional[str] = None

@dataclass
class Agents:
    vars: Dict[str, Any] = field(default_factory=dict)
    entry: Optional[Entry] = None

@dataclass
class Flows:
    entry: Optional[Entry] = None

@dataclass
class RequestAttributes:
    save_query: bool = False
    agents: Optional[Agents] = None
    flows: Optional[Flows] = None