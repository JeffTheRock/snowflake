
from __future__ import annotations

from dataclasses import dataclass
import app.engine as Engine

@dataclass
class Asset:
    index: int
    name: str
    url: str

    def __eq__(self, asset: "Asset") -> bool:
        return self.index == asset.index

    def __hash__(self) -> int:
        return hash(self.index)

    @classmethod
    def from_name(cls, name: str) -> "Asset" | None:
        return Engine.Instance.assets.by_name(name)
