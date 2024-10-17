from typing import Dict

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

compute_metric_key_map: Dict[str, str] = {
    "CPUUtilization": COMPUTE_CPU_UTIL,
    "DiskBytesRead": COMPUTE_DISK_READ_BYTES,
    "DiskBytesWritten": COMPUTE_DISK_WRITE_BYTES,
    "DiskIopsRead": COMPUTE_DISK_READ_IO,
    "DiskIopsWritten": COMPUTE_DISK_WRITE_IO,
    "LoadAverage": COMPUTE_LOAD,
    "MemoryAllocationStalls": COMPUTE_MEM_ALLOCATION_STALLS,
    "MemoryUtilization": COMPUTE_MEM_UTIL,
    "NetworksBytesIn": COMPUTE_NETWORK_RECEIVE,
    "NetworksBytesOut": COMPUTE_NETWORK_TRANSMIT,
}

# ------------------------------
#  End oci_computeagent metrics
# ------------------------------

namespace_map: Dict[str, Dict[str, str]] = {
    "oci_computeagent": compute_metric_key_map
}