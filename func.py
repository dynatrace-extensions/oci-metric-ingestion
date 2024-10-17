import io
import json
import logging
from typing import Dict
from MetricMapping import namespace_map

def process_metrics(body: Dict):
    logging.getLogger().info(f"process_metrics: {body}")

    namespace = body.get("namespace")
    resource_group = body.get("resourceGroup")
    compartment_id = body.get("compartmentId")
    metric_name = body.get("name")
    
    dimensions = body.get("dimensions", {})
    resource_id = dimensions.get("resourceId")
    attachment_id = dimensions.get("attachmentId")

    datapoints = body.get("datapoints")

    metric_map = namespace_map.get(namespace)
    dynatrace_metric_key = metric_map.get(metric_name)



def handler(ctx, data: io.BytesIO=None):
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
