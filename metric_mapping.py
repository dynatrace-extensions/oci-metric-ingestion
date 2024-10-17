from typing import Callable, Dict, List, Tuple, Optional
from aggregation import (
    AggregateResult,
    aggregate_max,
    aggregate_mean,
    aggregate_sum,
    aggregate_min,
)

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
    def value_from_oci_metric_name(
        self, oci_metric_name: str, datapoints: List[Dict]
    ) -> Optional[Tuple[str, AggregateResult]]:
        metric_mapping = self.metric_key_map.get(oci_metric_name)
        if metric_mapping is None:
            return None

        dynatrace_metric_key, aggregation_function = metric_mapping

        return dynatrace_metric_key, aggregation_function(datapoints)


""" All compute metric names imported by extension. """
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

""" All load balancer metric names imported by extension. """
LB_HTTP_REQUESTS = "cloud.oci.load_balancer.http.requests"
LB_ACTIVE_CONNECTIONS = "cloud.oci.load_balancer.active.connections"
LB_ACTIVE_SSL_CONNECTIONS = "cloud.oci.load_balancer.active.ssl.connections"
LB_BYTES_RECEIVED = "cloud.oci.load_balancer.bytes.received"
LB_BYTES_SENT = "cloud.oci.load_balancer.bytes.sent"
LB_ACCEPTED_CONNECTIONS = "cloud.oci.load_balancer.accepted.connections"
LB_HANDLED_CONNECTIONS = "cloud.oci.load_balancer.handled.connections"
LB_FAILED_SSL_HANDSHAKE = "cloud.oci.load_balancer.failed.ssl.handshake"
LB_ACCEPTED_SSL_HANDSHAKE = "cloud.oci.load_balancer.accepted.ssl.handshake"
LB_FAILED_SSL_CLIENT_CERT_VERIFY = (
    "cloud.oci.load_balancer.failed.ssl.client.cert.verify"
)
LB_PEAK_BANDWIDTH = "cloud.oci.load_balancer.peak.bandwidth"
LB_HTTP_RESPONSES = "cloud.oci.load_balancer.http.responses"
LB_HTTP_RESPONSES_200 = "cloud.oci.load_balancer.http.responses.200"
LB_HTTP_RESPONSES_2XX = "cloud.oci.load_balancer.http.responses.2xx"
LB_HTTP_RESPONSES_3XX = "cloud.oci.load_balancer.http.responses.3xx"
LB_HTTP_RESPONSES_4XX = "cloud.oci.load_balancer.http.responses.4xx"
LB_HTTP_RESPONSES_5XX = "cloud.oci.load_balancer.http.responses.5xx"
LB_HTTP_RESPONSES_502 = "cloud.oci.load_balancer.http.responses.502"
LB_HTTP_RESPONSES_504 = "cloud.oci.load_balancer.http.responses.504"
LB_BACKEND_SERVERS = "cloud.oci.load_balancer.backend.servers"
LB_UNHEALTHY_BACKEND_SERVERS = "cloud.oci.load_balancer.unhealthy.backend.servers"
LB_RESPONSE_TIME_HTTP = "cloud.oci.load_balancer.response.time.http"
LB_RESPONSE_TIME_TCP = "cloud.oci.load_balancer.response.time.tcp"
LB_BACKEND_TIMEOUTS = "cloud.oci.load_balancer.backend.timeouts"
LB_INVALID_HEADER_RESPONSES = "cloud.oci.load_balancer.invalid.header.responses"
LB_KEEPALIVE_CONNECTIONS = "cloud.oci.load_balancer.keepalive.connections"
LB_CLOSED_CONNECTIONS = "cloud.oci.load_balancer.closed.connections"

""" All network load balancer metric names imported by extension. """
NETLB_PROCESSED_BYTES = "cloud.oci.network_load_balancer.processed.bytes"
NETLB_PROCESSED_PACKETS = "cloud.oci.network_load_balancer.processed.packets"
NETLB_INGRESS_PACKETS_DROPPED = (
    "cloud.oci.network_load_balancer.ingress.packets.dropped"
)
NETLB_EGRESS_PACKETS_DROPPED = "cloud.oci.network_load_balancer.egress.packets.dropped"
NETLB_HEALTHY_BACKENDS = "cloud.oci.network_load_balancer.healthy.backends"
NETLB_UNHEALTHY_BACKENDS = "cloud.oci.network_load_balancer.unhealthy.backends"
NETLB_NEW_CONNECTIONS = "cloud.oci.network_load_balancer.new.connections"
NETLB_NEW_CONNECTIONS_TCP = "cloud.oci.network_load_balancer.new.connections.tcp"
NETLB_NEW_CONNECTIONS_UDP = "cloud.oci.network_load_balancer.new.connections.udp"

""" All VCN metric names imported by extension. """
VCN_INGRESS_PACKETS_DROPPED_SL = "cloud.oci.vcn.ingress.packets.dropped.sl"
VCN_EGRESS_PACKETS_DROPPED_SL = "cloud.oci.vcn.egress.packets.dropped.sl"
VCN_PACKETS_FROM_NETWORK = "cloud.oci.vcn.packets.from.network"
VCN_PACKETS_TO_NETWORK = "cloud.oci.vcn.packets.to.network"
VCN_BYTES_FROM_NETWORK = "cloud.oci.vcn.bytes.from.network"
VCN_BYTES_TO_NETWORK = "cloud.oci.vcn.bytes.to.network"
VCN_THROTTLED_INGRESS_PACKETS = "cloud.oci.vcn.throttled.ingress.packets"
VCN_THROTTLED_EGRESS_PACKETS = "cloud.oci.vcn.throttled.egress.packets"
VCN_INGRESS_PACKETS_DROPPED_FCTT = "cloud.oci.vcn.ingress.packets.dropped.fctt"
VCN_EGRESS_PACKETS_DROPPED_FCTT = "cloud.oci.vcn.egress.packets.dropped.fctt"
VCN_CTT_UTIL = "cloud.oci.vcn.ctt.util"
VCN_CTT_FULL = "cloud.oci.vcn.ctt.full"

""" All VPN metric names imported by extension. """
VPN_TUNNEL_STATE = "cloud.oci.vpn.tunnel_state"
VPN_PACKETS_RECEIVED = "cloud.oci.vpn.packets_received"
VPN_BYTES_RECEIVED = "cloud.oci.vpn.bytes_received"
VPN_PACKETS_SENT = "cloud.oci.vpn.packets_sent"
VPN_BYTES_SENT = "cloud.oci.vpn.bytes_sent"
VPN_PACKETS_ERROR = "cloud.oci.vpn.packets_error"

""" All block volume metric names imported by extension. """
BLOCKVOL_READ_THROUGHPUT = "cloud.oci.block_volume.read.throughput"
BLOCKVOL_WRITE_THROUGHPUT = "cloud.oci.block_volume.write.throughput"
BLOCKVOL_READ_OPS = "cloud.oci.block_volume.read.ops"
BLOCKVOL_WRITE_OPS = "cloud.oci.block_volume.write.ops"
BLOCKVOL_THROTTLED_IO = "cloud.oci.block_volume.throttled.ops"


""" All object storage metric names imported by extension. """
BUCKET_SIZE = "cloud.oci.object_store.size"
OBJECT_COUNT = "cloud.oci.object_store.count"

""" All instance pool metric names imported by extension. """
INSTANCE_POOL_SIZE = "cloud.oci.instance_pool.size"
INSTANCE_POOL_INSTANCES_PROVISIONING = "cloud.oci.instance_pool.provisioning"
INSTANCE_POOL_INSTANCES_RUNNING = "cloud.oci.instance_pool.running"
INSTANCE_POOL_INSTANCES_TERMINATED = "cloud.oci.instance_pool.terminated"

""" All filesystem metric names imported by extension. """
FS_READ_THROUGHPUT = "cloud.oci.filesystem.read.throughput"
FS_WRITE_THROUGHPUT = "cloud.oci.filesystem.write.throughput"
FS_READ_REQUESTS = "cloud.oci.filesystem.read.requests"
FS_WRITE_REQUESTS = "cloud.oci.filesystem.write.requests"
FS_READ_LATENCY = "cloud.oci.filesystem.read.latency"
FS_WRITE_LATENCY = "cloud.oci.filesystem.write.latency"
FS_METADATA_READ_LATENCY = "cloud.oci.filesystem.metadata.read.latency"
FS_METADATA_WRITE_LATENCY = "cloud.oci.filesystem.metadata.write.latency"
FS_METADATA_IOPS = "cloud.oci.filesystem.metadata.iops"
FS_USAGE = "cloud.oci.filesystem.usage"

""" All API Gateway metric names imported by extension. """
API_GATEWAY_HTTP_REQUESTS = "cloud.oci.api_gateway.http_requests"
API_GATEWAY_HTTP_RESPONSES = "cloud.oci.api_gateway.http_responses"
API_GATEWAY_BYTES_SENT = "cloud.oci.api_gateway.bytes_sent"
API_GATEWAY_BYTES_RECEIVED = "cloud.oci.api_gateway.bytes_received"
API_GATEWAY_LATENCY = "cloud.oci.api_gateway.latency"
API_GATEWAY_INTERNAL_LATENCY = "cloud.oci.api_gateway.internal_latency"
API_GATEWAY_INTEGRATION_LATENCY = "cloud.oci.api_gateway.integration_latency"
API_GATEWAY_BACKEND_HTTP_RESPONSES = "cloud.oci.api_gateway.backend_http_responses"
API_GATEWAY_USAGE_PLAN_REQUESTS = "cloud.oci.api_gateway.usage_plan_requests"
API_GATEWAY_SUBSCRIBER_REQUESTS = "cloud.oci.api_gateway.subscriber_requests"
API_GATEWAY_SUBSCRIBER_QUOTA_PROPORTION_USED = (
    "cloud.oci.api_gateway.subscriber_quota_proportion_used"
)
API_GATEWAY_SUBSCRIBER_RATE_LIMIT_PROPORTION_USED = (
    "cloud.oci.api_gateway.subscriber_rate_limit_proportion_used"
)

""" All Function metric names imported by the extension. """
FUNCTION_INVOCATION_COUNT = "cloud.oci.function.function_invocation_count"
FUNCTION_EXECUTION_DURATION = "cloud.oci.function.function_execution_duration"
FUNCTION_ERROR_RESPONSE_COUNT = "cloud.oci.function.function_error_response_count"
FUNCTION_THROTTLED_RESPONSE_COUNT = (
    "cloud.oci.function.function_throttled_response_count"
)

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
    ),
    "oci_lbaas": MetricMapping(
        metric_key_map={
            "HttpRequests": (LB_HTTP_REQUESTS, aggregate_mean),
            "ActiveConnections": (LB_ACTIVE_CONNECTIONS, aggregate_mean),
            "ActiveSSLConnections": (LB_ACTIVE_SSL_CONNECTIONS, aggregate_mean),
            "BytesReceived": (LB_BYTES_RECEIVED, aggregate_mean),
            "BytesSent": (LB_BYTES_SENT, aggregate_mean),
            "AcceptedConnections": (LB_ACCEPTED_CONNECTIONS, aggregate_mean),
            "HandledConnections": (LB_HANDLED_CONNECTIONS, aggregate_mean),
            "FailedSSLHandshake": (LB_FAILED_SSL_HANDSHAKE, aggregate_mean),
            "AcceptedSSLHandshake": (LB_ACCEPTED_SSL_HANDSHAKE, aggregate_mean),
            "FailedSSLClientCertVerify": (
                LB_FAILED_SSL_CLIENT_CERT_VERIFY,
                aggregate_sum,
            ),
            "PeakBandwidth": (LB_PEAK_BANDWIDTH, aggregate_mean),
            "HttpResponses": (LB_HTTP_RESPONSES, aggregate_mean),
            "HttpResponses200": (LB_HTTP_RESPONSES_200, aggregate_mean),
            "HttpResponses2xx": (LB_HTTP_RESPONSES_2XX, aggregate_mean),
            "HttpResponses3xx": (LB_HTTP_RESPONSES_3XX, aggregate_mean),
            "HttpResponses4xx": (LB_HTTP_RESPONSES_4XX, aggregate_mean),
            "HttpResponses5xx": (LB_HTTP_RESPONSES_5XX, aggregate_mean),
            "HttpResponses502": (LB_HTTP_RESPONSES_502, aggregate_mean),
            "HttpResponses504": (LB_HTTP_RESPONSES_504, aggregate_mean),
            "BackendServers": (LB_BACKEND_SERVERS, aggregate_min),
            "UnHealthyBackendServers": (LB_UNHEALTHY_BACKEND_SERVERS, aggregate_max),
            "ResponseTimeHttpHeader": (LB_RESPONSE_TIME_HTTP, aggregate_max),
            "ResponseTimeFirstByte": (LB_RESPONSE_TIME_TCP, aggregate_max),
            "BackendTimeouts": (LB_BACKEND_TIMEOUTS, aggregate_mean),
            "InvalidHeaderResponses": (LB_INVALID_HEADER_RESPONSES, aggregate_sum),
            "KeepaliveConnections": (LB_KEEPALIVE_CONNECTIONS, aggregate_mean),
            "ClosedConnections": (LB_CLOSED_CONNECTIONS, aggregate_sum),
        },
        dimension_map={
            "availabilityDomain": "oci.availability_domain",
            "lbComponent": "lb_component",
            "lbHostId": "lb_host_id",
            "region": "oci.region",
            "lbName": "oci.resource_display_name",
            "resourceId": "oci.resource_id",
            "resourceGroup": "oci.resource_group",
            "compartmentId": "oci.compartment_id",
            "backendSetName": "backend_set_name",
        },
        constant_dimension_map={
            "cloud.provider": "oci",
            "oci.service": "load_balancer",
        },
    ),
    "oci_nlb": MetricMapping(
        metric_key_map={
            "ProcessedBytes": (NETLB_PROCESSED_BYTES, aggregate_sum),
            "ProcessedPackets": (NETLB_PROCESSED_PACKETS, aggregate_sum),
            "IngressPacketsDroppedBySL": (NETLB_INGRESS_PACKETS_DROPPED, aggregate_sum),
            "EgressPacketsDroppedBySL": (NETLB_EGRESS_PACKETS_DROPPED, aggregate_sum),
            "HealthyBackendsPerNlb": (NETLB_HEALTHY_BACKENDS, aggregate_sum),
            "UnhealthyBackendsPerNlb": (NETLB_UNHEALTHY_BACKENDS, aggregate_sum),
            "NewConnections": (NETLB_NEW_CONNECTIONS, aggregate_sum),
            "NewConnectionsTCP": (NETLB_NEW_CONNECTIONS_TCP, aggregate_sum),
            "NewConnectionsUDP": (NETLB_NEW_CONNECTIONS_UDP, aggregate_sum),
        },
        dimension_map={
            "region": "oci.region",
            "resourceName": "oci.resource_display_name",
            "resourceId": "oci.resource_id",
            "resourceGroup": "oci.resource_group",
            "compartmentId": "oci.compartment_id",
        },
        constant_dimension_map={
            "cloud.provider": "oci",
            "oci.service": "network_load_balancer",
        },
    ),
    "oci_vcn": MetricMapping(
        metric_key_map={
            "VnicIngressDropsSecurityList": (
                VCN_INGRESS_PACKETS_DROPPED_SL,
                aggregate_sum,
            ),
            "VnicEgressDropsSecurityList": (
                VCN_EGRESS_PACKETS_DROPPED_SL,
                aggregate_sum,
            ),
            "VnicFromNetworkPackets": (VCN_PACKETS_FROM_NETWORK, aggregate_sum),
            "VnicToNetworkPackets": (VCN_PACKETS_TO_NETWORK, aggregate_sum),
            "VnicFromNetworkBytes": (VCN_BYTES_FROM_NETWORK, aggregate_sum),
            "VnicToNetworkBytes": (VCN_BYTES_TO_NETWORK, aggregate_sum),
            "VnicIngressDropsThrottle": (VCN_THROTTLED_INGRESS_PACKETS, aggregate_sum),
            "VnicEgressDropsThrottle": (VCN_THROTTLED_EGRESS_PACKETS, aggregate_sum),
            "VnicIngressDropsConntrackFull": (
                VCN_INGRESS_PACKETS_DROPPED_FCTT,
                aggregate_sum,
            ),
            "VnicEgressDropsConntrackFull": (
                VCN_EGRESS_PACKETS_DROPPED_FCTT,
                aggregate_sum,
            ),
            "VnicConntrackUtilPercent": (VCN_CTT_UTIL, aggregate_sum),
            "VnicConntrackIsFull": (VCN_CTT_FULL, aggregate_sum),
        },
        dimension_map={
            "region": "oci.region",
            # "resourceId": "oci.resource_display_name",
            # "resourceId": "vnic_id",
            "resourceId": "oci.resource_id",
            "resourceGroup": "oci.resource_group",
            "compartmentId": "oci.compartment_id",
        },
        constant_dimension_map={
            "cloud.provider": "oci",
            "oci.service": "vcn",
        },
    ),
    "oci_vpn": MetricMapping(
        metric_key_map={
            "TunnelState": (VPN_TUNNEL_STATE, aggregate_sum),
            "PacketsReceived": (VPN_PACKETS_RECEIVED, aggregate_sum),
            "BytesReceived": (VPN_BYTES_RECEIVED, aggregate_sum),
            "PacketsSent": (VPN_PACKETS_SENT, aggregate_sum),
            "BytesSent": (VPN_BYTES_SENT, aggregate_sum),
            "PacketsError": (VPN_PACKETS_ERROR, aggregate_sum),
        },
        dimension_map={
            "region": "oci.region",
            "parentResourceId": "oci.resource_id",
            "resourceGroup": "oci.resource_group",
            "compartmentId": "oci.compartment_id",
            "publicIp": "vpn.public_ip",
        },
        constant_dimension_map={
            "cloud.provider": "oci",
            "oci.service": "vpn",
        },
    ),
    "oci_blockstore": MetricMapping(
        metric_key_map={
            "VolumeReadThroughput": (BLOCKVOL_READ_THROUGHPUT, aggregate_mean),
            "VolumeWriteThroughput": (BLOCKVOL_WRITE_THROUGHPUT, aggregate_mean),
            "VolumeReadOps": (BLOCKVOL_READ_OPS, aggregate_mean),
            "VolumeWriteOps": (BLOCKVOL_WRITE_OPS, aggregate_mean),
            "VolumeThrottledIOs": (BLOCKVOL_THROTTLED_IO, aggregate_sum),
        },
        dimension_map={
            "region": "oci.region",
            "resourceId": "oci.resource_id",
            "attachmentId": "attachment_id",
            "resourceGroup": "oci.resource_group",
            "compartmentId": "oci.compartment_id",
        },
        constant_dimension_map={
            "cloud.provider": "oci",
            "oci.service": "block_volume",
        },
    ),
    # "oci_objectstore": MetricMapping(
    #     metric_key_map={
    #     'StoredBytes[60m]{tier = "%s"}.sum()': (BUCKET_SIZE),
    #     'ObjectCount[60m]{tier = "%s"}.sum()': (OBJECT_COUNT),
    #     }
    # )
    "oci_instancepools": MetricMapping(
        metric_key_map={
            "InstancePoolSize": (INSTANCE_POOL_SIZE, aggregate_sum),
            "ProvisioningInstances": (
                INSTANCE_POOL_INSTANCES_PROVISIONING,
                aggregate_sum,
            ),
            "RunningInstances": (INSTANCE_POOL_INSTANCES_RUNNING, aggregate_sum),
            "TerminatedInstances": (INSTANCE_POOL_INSTANCES_TERMINATED, aggregate_sum),
        },
        dimension_map={
            "DisplayName": "oci.resource_display_name",
            "region": "oci.region",
            "resourceId": "oci.resource_id",
            "compartmentId": "oci.compartment_id",
            "resourceGroup": "oci.resource_group",
        },
        constant_dimension_map={
            "cloud.provider": "oci",
            "oci.service": "instance_pool",
        },
    ),
    # "oci_filestorage": MetricMapping(
    #     metric_key_map={
    #         'FileSystemReadThroughput[1m]{resourceType = "filesystem"}': (FS_READ_THROUGHPUT, aggregate_mean),
    #         'FileSystemWriteThroughput[1m]{resourceType = "filesystem"}': (FS_WRITE_THROUGHPUT, aggregate_mean),
    #         'FileSystemReadRequestsbySize[1m]{resourceType = "filesystem"}': (FS_READ_REQUESTS, aggregate_mean),
    #         'FileSystemWriteRequestsbySize[1m]{resourceType = "filesystem"}': (FS_WRITE_REQUESTS, aggregate_mean),
    #         'FileSystemReadAverageLatencybySize[1m]{resourceType = "filesystem"}': (FS_READ_LATENCY, aggregate_mean),
    #         'FileSystemWriteAverageLatencybySize[1m]{resourceType = "filesystem"}': (FS_WRITE_LATENCY, aggregate_mean),
    #         'MetadataRequestAverageLatency[1m]{resourceType = "filesystem", operation = "ReadMetadata"}': (FS_METADATA_READ_LATENCY, aggregate_mean),
    #         'MetadataRequestAverageLatency[1m]{resourceType = "filesystem", operation = "WriteMetadata"}': (FS_METADATA_WRITE_LATENCY, aggregate_mean),
    #         'MetadataIOPS[1m]{resourceType = "filesystem"}': (FS_METADATA_IOPS, aggregate_mean),
    #         'FileSystemUsage[60m]{resourceType = "filesystem"}': (FS_USAGE, aggregate_mean),
    #     }
    # )
    "oci_apigateway": MetricMapping(
        metric_key_map={
            "HttpRequests": (API_GATEWAY_HTTP_REQUESTS, aggregate_sum),
            "HttpResponses": (API_GATEWAY_HTTP_RESPONSES, aggregate_sum),
            "BytesSent": (API_GATEWAY_BYTES_SENT, aggregate_sum),
            "BytesReceived": (API_GATEWAY_BYTES_RECEIVED, aggregate_sum),
            "Latency": (API_GATEWAY_LATENCY, aggregate_mean),
            "InternalLatency": (API_GATEWAY_INTERNAL_LATENCY, aggregate_mean),
            "IntegrationLatency": (API_GATEWAY_INTEGRATION_LATENCY, aggregate_mean),
            "BackendHttpResponses": (API_GATEWAY_BACKEND_HTTP_RESPONSES, aggregate_sum),
            "UsagePlanRequests": (API_GATEWAY_USAGE_PLAN_REQUESTS, aggregate_sum),
            "SubscriberRequests": (API_GATEWAY_SUBSCRIBER_REQUESTS, aggregate_sum),
            "SubscriberQuotaProportionUsed": (
                API_GATEWAY_SUBSCRIBER_QUOTA_PROPORTION_USED,
                aggregate_mean,
            ),
            "SubscriberRateLimitProportionUsed": (
                API_GATEWAY_SUBSCRIBER_RATE_LIMIT_PROPORTION_USED,
                aggregate_mean,
            ),
        },
        dimension_map={
            "resourceName": "oci.resource_display_name",
            "region": "oci.region",
            "resourceId": "oci.resource_id",
            "compartmentId": "oci.compartment_id",
            "resourceGroup": "oci.resource_group",
            "resourceTenantId": "oci.tenancy_id"
        },
        constant_dimension_map={
            "cloud.provider": "oci",
            "oci.service": "api_gateway",
        },
    ),
    "oci_faas": MetricMapping(
        metric_key_map={
        "FunctionInvocationCount": (FUNCTION_INVOCATION_COUNT, aggregate_sum),
        "FunctionExecutionDuration": (FUNCTION_EXECUTION_DURATION, aggregate_mean),
        # 'FunctionResponseCount[1m]{responseType = "Error"}.sum()': (FUNCTION_ERROR_RESPONSE_COUNT),
        # 'FunctionResponseCount[1m]{responseType = "Throttled"}.sum()': (FUNCTION_THROTTLED_RESPONSE_COUNT),
        },
        dimension_map={
            "resourceDisplayName": "oci.resource_display_name",
            "region": "oci.region",
            "resourceId": "oci.resource_id",
            "compartmentId": "oci.compartment_id",
            "resourceGroup": "oci.resource_group",
            "resourceTenantId": "oci.tenancy_id"
        },
        constant_dimension_map={
            "cloud.provider": "oci",
            "oci.service": "function",
        },
    )
}
