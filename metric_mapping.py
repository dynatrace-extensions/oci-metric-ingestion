from typing import Callable, Dict, List, Tuple, Optional
from aggregation import AggregateResult, aggregate_max


class MetricMapping:
    def __init__(
        self,
        metric_key_map: Dict[str, Tuple[str, Callable[[List[Dict]], AggregateResult]]],
        dimension_map: Dict[str, str],
        constant_dimension_map: Dict[str, str] = {},
    ):
        self.metric_key_map = metric_key_map
        self.dimension_map = dimension_map
        self.constant_dimension_map = constant_dimension_map

    # Given the list of OCI dimensions, this function maps the dimension keys to Dynatrace dimensions
    def dimensions(self, oci_dimensions: Dict[str, str]) -> Dict[str, str]:
        dimensions = self.constant_dimension_map.copy()
        for key, value in oci_dimensions.items():
            dynatrace_dimension_key = self.dimension_map.get(key)
            if dynatrace_dimension_key:
                dimensions[dynatrace_dimension_key] = value
        return dimensions
    
    # Given the oci metric name and the list of datapoints, this function returns the dynatrace metric name and the aggregated value
    def value_from_oci_metric_name(self, oci_metric_name: str, datapoints: List[Dict]) -> Optional[Tuple[str, AggregateResult]]:
        metric_mapping = self.metric_key_map.get(oci_metric_name)
        if metric_mapping is None:
            return None
        
        dynatrace_metric_key, aggregation_function = metric_mapping

        return dynatrace_metric_key, aggregation_function(datapoints)

# ------------------------------
# Start oci_computeagent metrics
# ------------------------------
COMPUTE_CPU_UTIL = "cloud.oci.compute.cpu.util"
COMPUTE_DISK_READ_BYTES = "cloud.oci.compute.disk.read.bytes"
COMPUTE_DISK_WRITE_BYTES = "cloud.oci.compute.disk.write.bytes"
COMPUTE_DISK_READ_IO = "cloud.oci.compute.disk.read.io"
COMPUTE_DISK_WRITE_IO = "cloud.oci.compute.disk.write.io"
COMPUTE_LOAD = "cloud.oci.compute.load"
COMPUTE_MEM_ALLOCATION_STALLS = "cloud.oci.compute.memory.allocation.stalls"
COMPUTE_MEM_UTIL = "cloud.oci.compute.memory.util"
COMPUTE_NETWORK_RECEIVE = "cloud.oci.compute.network.receive.bytes"
COMPUTE_NETWORK_TRANSMIT = "cloud.oci.compute.network.transmit.bytes"
# ------------------------------
#  End oci_computeagent metrics
# ------------------------------

namespace_map: Dict[str, MetricMapping] = {
    "oci_computeagent": MetricMapping(
        metric_key_map={
            "CPUUtilization": (COMPUTE_CPU_UTIL, aggregate_max),
            "DiskBytesRead": (COMPUTE_DISK_READ_BYTES, aggregate_max),
            "DiskBytesWritten": (COMPUTE_DISK_WRITE_BYTES, aggregate_max),
            "DiskIopsRead": (COMPUTE_DISK_READ_IO, aggregate_max),
            "DiskIopsWritten": (COMPUTE_DISK_WRITE_IO, aggregate_max),
            "LoadAverage": (COMPUTE_LOAD, aggregate_max),
            "MemoryAllocationStalls": (COMPUTE_MEM_ALLOCATION_STALLS, aggregate_max),
            "MemoryUtilization": (COMPUTE_MEM_UTIL, aggregate_max),
            "NetworksBytesIn": (COMPUTE_NETWORK_RECEIVE, aggregate_max),
            "NetworksBytesOut": (COMPUTE_NETWORK_TRANSMIT, aggregate_max),
        },
        dimension_map={
            "availabilityDomain": "oci.availability_domain",
            "faultDomain": "oci.fault_domain",
            "imageId": "image_id",
            "instancePoolId": "instance_pool_id",
            "region": "oci.region",
            "resourceDisplayName": "oci.resource_display_name",
            "resourceId": "oci.resource_id",
            "resourceGroup": "oci.resource_group",
            "compartmentId": "oci.compartment_id",
        },
        constant_dimension_map={"cloud.provider": "oci", "oci.service": "compute"},
    )
}
