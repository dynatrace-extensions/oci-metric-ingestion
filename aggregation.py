from collections import defaultdict
from datetime import datetime, timezone
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class AggregateResult:
    timestamp: int
    value: int

def create_minutely_buckets(datapoints: List[Dict]) -> Dict[float, list]:
    buckets = defaultdict(list)

    for point in datapoints:
        ts_ms = point["timestamp"]
        dt = datetime.fromtimestamp(ts_ms / 1000, timezone.utc)
        minute_bucket = int(dt.replace(second=0, microsecond=0).timestamp())
        buckets[minute_bucket].append(point["value"])
    return buckets

def aggregate_max(datapoints: List[Dict]) -> List[AggregateResult]:
    buckets = create_minutely_buckets(datapoints)

    aggregated = []
    for timestamp, values in sorted(buckets.items()):
        aggregated.append(AggregateResult(timestamp, max(values)))
    return aggregated

def aggregate_min(datapoints: List[Dict]) -> List[AggregateResult]:
    buckets = create_minutely_buckets(datapoints)

    aggregated = []
    for timestamp, values in sorted(buckets.items()):
        aggregated.append(AggregateResult(timestamp, min(values)))
    return aggregated

def aggregate_sum(datapoints: List[Dict]) -> List[AggregateResult]:
    buckets = create_minutely_buckets(datapoints)

    aggregated = []
    for timestamp, values in sorted(buckets.items()):
        aggregated.append(AggregateResult(timestamp, sum(values)))
    return aggregated

def aggregate_mean(datapoints: List[Dict]) -> List[AggregateResult]:
    buckets = create_minutely_buckets(datapoints)

    aggregated = []
    for timestamp, values in sorted(buckets.items()):
        aggregated.append(AggregateResult(timestamp, sum(values) / len(values)))
    return aggregated
 
