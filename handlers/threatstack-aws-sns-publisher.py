# Receive a webhook from Threat Stack, lookup alert detail, and publish to
# an SNS topic.
import boto3
import json
import logging
import os
from threatstack import ThreatStack

log_level = os.environ.get('LOG_LEVEL', 'INFO')
logging.root.setLevel(logging.getLevelName(log_level))
_logger = logging.getLogger(__name__)

# Initialize client.
THREATSTACK_API_KEY = os.environ.get('THREATSTACK_API_KEY')
THREATSTACK_ORG_ID  = os.environ.get('THREATSTACK_ORG_ID')
THREATSTACK_USER_ID  = os.environ.get('THREATSTACK_USER_ID')

threatstack_client = ThreatStack(
    api_key=THREATSTACK_API_KEY,
    org_id=THREATSTACK_ORG_ID,
    user_id=THREATSTACK_USER_ID
)

# Initialize AWS client
AWS_SNS_TOPIC_ARN = os.environ.get('AWS_SNS_TOPIC_ARN')
sns_client = boto3.client('sns')

def _get_alert(alert_id):
    '''Return an alert from Threat Stack by ID.'''
    return threatstack_client.alerts.get(alert_id)


def _get_alerts(webhook):
    '''Return the data for alerts from a Threat Stack Webhook.'''
    webhook_body_data = json.loads(webhook)
    webhook_alert_list = webhook_body_data.get('alerts')

    # A webhook may contain multiple alerts.  Loop through and fetch alert
    # data for each.
    alert_list = []
    for webhook_alert in webhook_alert_list:
        alert_id = webhook_alert.get('id')
        alert = _get_alert(alert_id)
        _logger.debug('alert: {}'.format(json.dumps(alert)))
        alert_list.append(alert)

    return alert_list


def _publish_alert(alert):
    '''Publish an alert to SNS'''
    response = sns_client.publish(
        TopicArn=AWS_SNS_TOPIC_ARN,
        Message=json.dumps(alert)
    )
    return response


def handler(event, context):
    _logger.debug('event: {}'.format(json.dumps(event)))
    event_body = event.get('body')
    _logger.info('event.body: {}'.format(event_body))

    # Get alerts from Threat Stack
    alert_list = _get_alerts(event_body)

    # Publish each alert to SNS.
    sns_response_list = []
    for alert in alert_list:
        sns_response = _publish_alert(alert)
        sns_response_list.append(response)

    # Return repsonse
    response_body = {
        'sns_responses': sns_response_list
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(response_body)
    }

    return response

