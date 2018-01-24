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

def _get_alert(webhook):
    '''Return an alert from Threat Stack by ID.'''
    alert_id = webhook.get('id')
    return threatstack_client.alerts.get(alert_id)


def _get_events_from_alert(alert):
    '''Return a list of event detail from Threat stack alert.'''
    alert_id = alert.get('id')
    return threatstack_client.alerts.events(alert_id).get('events', [])


def _get_rule_from_alert(alert):
    '''Return a rule from a Threat Stack alert.'''
    rule_id = alert.get('ruleId')
    ruleset_id = alert.get('rulesetId')
    return threatstack_client.rulesets.rules(ruleset_id, rule_id)


def _get_ruleset_from_alert(alert):
    '''Return a ruleset from a Threat Stack alert.'''
    ruleset_id = alert.get('rulesetId')
    return threatstack_client.rulesets.get(ruleset_id)


def _get_alert_detail(webhook_alert):
    '''Return the data for alerts from a Threat Stack Webhook.'''
    _logger.debug('_get_alert_detail(): webhook_alert={}'.format(json.dumps(webhook_alert)))
    alert_detail = {}

    alert = _get_alert(webhook_alert)
    alert_detail['alert'] = alert

    events = _get_events_from_alert(alert)
    alert_detail['events'] = events

    ruleset = _get_ruleset_from_alert(alert)
    alert_detail['ruleset'] = ruleset

    rule = _get_rule_from_alert(alert)
    alert_detail['rule'] = rule

    _logger.debug('_get_alert_detail(): alert_detail={}'.format(json.dumps(alert_detail)))
    return alert_detail


def _publish_alert(alert):
    '''Publish an alert to SNS'''
    response = sns_client.publish(
        TopicArn=AWS_SNS_TOPIC_ARN,
        Message=json.dumps(alert)
    )
    return response


def handler(event, context):
    _logger.debug('handler(): event={}'.format(json.dumps(event)))
    event_body = event.get('body')
    _logger.info('handler(): event.body={}'.format(event_body))
    # The data is a JSON string.
    webhook_data = json.loads(event_body)

    # Get alerts from Threat Stack
    webhook_alert_list = webhook_data.get('alerts')
    alert_detail_list = []
    for webhook_alert in webhook_alert_list:
        alert_detail = _get_alert_detail(webhook_alert)
        alert_detail_list.append(alert_detail)

    # Publish each alert to SNS.
    sns_response_list = []
    for alert in alert_detail_list:
        sns_response = _publish_alert(alert)
        sns_response_list.append(sns_response)

    # Return repsonse
    response_body = {
        'sns_responses': sns_response_list
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(response_body)
    }

    _logger.info('handler(): response={}'.format(json.dumps(response)))
    return response

