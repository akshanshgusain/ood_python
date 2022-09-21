from dataclasses import dataclass


@dataclass(frozen=True)
class Rider:
    id: str
    name: str
