from datetime import datetime
from summary_stat import SummaryStat
from typing import Dict, Optional, Union

class MintMetric(str):
    def __new__(cls, key: str, value: Union[float, SummaryStat], dimensions: Dict[str, str] | None = None, time: Optional[int] = None):
        if dimensions is None:
            dimensions = {}
        dimensions_string = ",".join(
            [f'{k.lower()}="{v}"' for k, v in dimensions.items()]
        )
        timestamp = int(datetime.now().timestamp() * 1000)
        if time is not None:
            timestamp = time
        return super().__new__(
            cls, f"{key}{',' if dimensions_string else ''}{dimensions_string} gauge,{value} {timestamp}"
        )