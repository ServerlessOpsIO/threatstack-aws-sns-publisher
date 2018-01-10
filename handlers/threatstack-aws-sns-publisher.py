# Receive a webhook from Threat Stack, lookup alert detail, and publish to
# an SNS topic.
import boto3
import json
import logging
import os

log_level = os.environ.get('LOG_LEVEL', 'INFO')
logging.root.setLevel(logging.getLevelName(log_level))
_logger = logging.getLogger(__name__)

def handler(event, context):
    _logger.debug('event: {}'.format(json.dumps(event)))

    event_body = json.loads(event.get('body'))
    _logger.info('event.body: {}'.format(json.dumps(event_body)))

    response_body = {
        "event_body": event_body
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(response_body)
    }

    return response

