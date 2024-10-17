from typing import Dict, Optional
from datetime import datetime

class MintMetric(str):
    def __new__(cls, key: str, value: float, dimensions: Dict[str, str] | None = None, time: Optional[int] = None):
        if dimensions is None:
            dimensions = {}
        dimensions_string = ",".join(
            [f'{k.lower()}="{v}"' for k, v in dimensions.items()]
        )
        timestamp = int(datetime.now().timestamp() * 1000)
        if time is not None:
            timestamp = time
        return super().__new__(
            cls, f"{key}{',' if dimensions_string else ''}{dimensions_string} {value} {timestamp}"
        )