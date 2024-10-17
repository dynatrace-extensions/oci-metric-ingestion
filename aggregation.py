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

def aggregate_min(datapoints: List[Dict]) -> AggregateResult:
    timestamp = sys.maxsize
    min_value = 0
    for datapoint in datapoints:
        timestamp = min(timestamp, datapoint.get("timestamp"))
        min_value = min(min_value, datapoint.get("value"))
    return AggregateResult(timestamp, min_value)

def aggregate_sum(datapoints: List[Dict]) -> AggregateResult:
    timestamp = sys.maxsize
    sum = 0
    for datapoint in datapoints:
        timestamp = min(timestamp, datapoint.get("timestamp"))
        sum += datapoint.get("value")
    return AggregateResult(timestamp, sum)

def aggregate_mean(datapoints: List[Dict]) -> AggregateResult:
    result = aggregate_sum(datapoints)
    return AggregateResult(result.timestamp, result.value / len(datapoints))
 
