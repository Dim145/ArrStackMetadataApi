from dataclasses import dataclass
from typing import Optional


@dataclass
class MediumResource:
    Name: Optional[str] = None
    Format: Optional[str] = None
    Position: int = 0