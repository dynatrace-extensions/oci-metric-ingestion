import sys
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class AggregateResult:
    timestamp: int
    value: int

def aggregate_max(datapoints: List[Dict]) -> AggregateResult:
    timestamp = sys.maxsize
    max_value = 0
    for datapoint in datapoints:
        timestamp = min(timestamp, datapoint.get("timestamp"))
        max_value = max(max_value, datapoint.get("value"))
    return AggregateResult(timestamp, max_value)