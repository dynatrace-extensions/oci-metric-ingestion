import io
import os
import json
import logging
import requests
from typing import Dict
from metric_mapping import namespace_map
from mint import MintMetric


def process_metrics(body: Dict):
    logging.getLogger().info(f"process_metrics: {body}")

    namespace = body.get("namespace")
    metric_name = body.get("name")

    oci_dimensions: Dict[str, str] = body.get("dimensions", {})

    # Include the resourceGroup and compartmentId in oci_dimensions so they can be mapped using the dimension_mapping
    oci_dimensions["resourceGroup"] = body.get("resourceGroup")
    oci_dimensions["compartmentId"] = body.get("compartmentId")

    datapoints = body.get("datapoints")

    metric_map = namespace_map.get(namespace)
    if metric_map is None:
        logging.getLogger().error(f"Could not find a metric mapping for namespace '{namespace}'")
        return

    value_or_none = metric_map.value_from_oci_metric_name(metric_name, oci_dimensions, datapoints)
    if value_or_none is None:
        logging.getLogger().error(f"Could not find a mapping for metric '{metric_name}' in namespace '{namespace}'")
        return

    dynatrace_metric_key, result = value_or_none
    dimensions = metric_map.dimensions(oci_dimensions)

    mint_metric = MintMetric(
        dynatrace_metric_key, result.value, dimensions, result.timestamp
    )
    logging.getLogger().info(f"process_metrics: Mint Metric: {mint_metric}")


METRIC_INGEST_ENDPOINT = "/api/v2/metrics/ingest"


def push_metrics_to_dynatrace(mint_metric: MintMetric):
    try:
        dynatrace_api_key = os.environ["DYNATRACE_API_KEY"]
        tenant_url = os.environ["DYNATRACE_TENANT"]

        # Remove the trailing slash if it exits
        if tenant_url.endswith("/"):
            tenant_url = tenant_url[:-1]

        # Append the log ingest endpoint to tenant url
        tenant_url = f"{tenant_url}{METRIC_INGEST_ENDPOINT}"
        headers = {
            "Content-Type": "text/plain",
            "Authorization": f"Api-Token {dynatrace_api_key}",
        }
        response = requests.post(tenant_url, data=str(mint_metric), headers=headers)
        logging.getLogger().info(response.text)
    except (Exception, ValueError) as ex:
        logging.getLogger().error(str(ex))


def handler(ctx, data: io.BytesIO = None):
    try:
        body = json.loads(data.getvalue())
        if isinstance(body, list):
            # Batch of CloudEvents format
            for b in body:
                process_metrics(b)
        else:
            # Single CloudEvent
            process_metrics(body)
    except (Exception, ValueError) as ex:
        logging.getLogger().error(str(ex))
