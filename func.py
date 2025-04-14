import io
import os
import json
import logging
from typing import Dict
from aggregation import create_minutely_buckets
from dynatrace_client import DynatraceClient
from mint import MintMetric
from summary_stat import SummaryStat
from metric_mapping import namespace_map


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
        logging.getLogger().error(
            f"Could not find a metric mapping for namespace '{namespace}'"
        )
        return

    import_all_metrics = True if os.environ["IMPORT_ALL_METRICS"] == "True" else False
    logging.getLogger().info(f"import_all_metrics: {import_all_metrics}")

    value_or_none = metric_map.value_from_oci_metric_name(
        metric_name, oci_dimensions, datapoints
    )
    if value_or_none is None:
        if import_all_metrics:
            key_namespace = namespace.replace("oci_", "")
            key = f"cloud.oci.{key_namespace}.{metric_name}"

            buckets = create_minutely_buckets(datapoints)
            aggregated = {}
            for timestamp, values in sorted(buckets.items()):
                aggregated[timestamp] = SummaryStat(min(values), max(values), sum(values), len(values))

            for timestamp, summary_stat in aggregated.items():
                mint_metric = MintMetric(
                    key,
                    summary_stat,
                    {
                        "oci.resource_group": oci_dimensions.get("resourceGroup"),
                        "oci.compartment_id": oci_dimensions.get("compartmentId"),
                    },
                    timestamp * 1000,
                )
                logging.getLogger().info(f"mint_metric: {mint_metric}")
                push_metrics_to_dynatrace(mint_metric)
        else:
            logging.getLogger().debug(
                f"Could not find a mapping for metric '{metric_name}' in namespace '{namespace}'"
            )

        return

    dynatrace_metric_key, results = value_or_none
    dimensions = metric_map.dimensions(oci_dimensions)

    for result in results:
        mint_metric = MintMetric(
            dynatrace_metric_key, result.value, dimensions, result.timestamp * 1000
        )
    logging.getLogger().info(f"process_metrics: Mint Metric: {mint_metric}")
    push_metrics_to_dynatrace(mint_metric)


METRIC_INGEST_ENDPOINT = "/api/v2/metrics/ingest"

def push_metrics_to_dynatrace(mint_metric: MintMetric):
    try:
        tenant_url = os.environ["DYNATRACE_TENANT"]
        # Remove the trailing slash if it exits
        if tenant_url.endswith("/"):
            tenant_url = tenant_url[:-1]
        client = DynatraceClient(tenant_url)

        auth_method = os.environ["AUTH_METHOD"]
        if auth_method == "oauth":
            client_id = os.environ["OAUTH_CLIENT_ID"]
            client_secret = os.environ["OAUTH_CLIENT_SECRET"]
            account_urn = os.environ["OAUTH_ACCOUNT_URN"]
            client.using_oauth(client_id, client_secret, account_urn)
        elif auth_method == "token":
            api_token = os.environ["DYNATRACE_API_KEY"]
            client.using_api_token(api_token)
        else:
            logging.getLogger().error(f"Invalid authentication method '{auth_method}'. Expected either 'oauth' or 'token'")

        client.send_mint_metric(str(mint_metric))
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
