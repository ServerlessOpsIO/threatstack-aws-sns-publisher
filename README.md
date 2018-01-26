# threatstack-aws-sns-publisher

[![Build Status](https://travis-ci.org/ServerlessOpsIO/threatstack-aws-sns-publisher.svg?branch=master)](https://travis-ci.org/ServerlessOpsIO/threatstack-aws-sns-publisher) [![License](https://img.shields.io/badge/License-BSD%202--Clause-orange.svg)](https://opensource.org/licenses/BSD-2-Clause)

Receives webhooks from Threat Stack and publishes alert details to an SNS topic.  Subsribe additional services to the SNS topic to aggregate alert data to multiple services.  To see example subscribers for this service, checkout our [GitHub org](https://github.com/ServerlessOpsIO?q=threatstack-)!

The service consists of:

* AWS API Gateway endpoint
* AWS Lambda function
* AWS SNS topic
* Permission resources to allow services to communicate

## Deployment
This service can be deployed using the button below which will redirect to CloudFormation.  You will need your Threat Stack API key, Org ID, User ID to deploy.

[![Launch CloudFormation Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](http://serverlessops-opensource-deploy-dev.s3-website-us-east-1.amazonaws.com/threatstack-aws-sns-publisher/CFN-DEPLOY-LATEST)

Alternatively, you can deploy from a clone of this repository by using [Serverless Framework](https://serverless.com/).

```
$ npm install -g serverless
$ npm install
$ THREATSTACK_API_KEY=<THREATSTACK_API_KEY> THREATSTACK_ORG_ID=<THREATSTACK_ORG_ID> THREATSTACK_USER_ID=<THREATSTACK_USER_ID> serverless deploy -v
```

## Configuration
After this service is deployed, obtained the _WebHookEndpoint_ output value from the stack and enter that as the webhook url on the Threat Stack integrations screen.

```
$ aws cloudformation describe-stacks --stack-name <STACK_NAME> --query "[Stacks][0][0].Outputs"
[
    {
        "OutputKey": "ThreatStackAwsSnsPublisherLambdaFunctionQualifiedArn",
        "OutputValue": "arn:aws:lambda:us-east-1:529602709954:function:threatstack-aws-sns-publisher-prime-ThreatStackAwsSnsPublisher:70",
        "Description": "Current Lambda function version"
    },
    {
        "OutputKey": "SnsConfirmSubscriptionIamManagedPolicyArn",
        "OutputValue": "arn:aws:iam::529602709954:policy/threatstack-aws-sns-publisher-prime-SnsConfirmSubscriptionIamManagedPolicy-9EHKMD539ZUP",
        "Description": "ARN of IAM managed policy for subscription confirmation",
        "ExportName": "threatstack-aws-sns-publisher-prime-SnsConfirmSubscriptionIamManagedPolicyArn"
    },
    {
        "OutputKey": "WebHookEndpoint",
        "OutputValue": "https://1f1axqumck.execute-api.us-east-1.amazonaws.com/prime/threatstack-aws-sns-publisher/api/v2/alert",
        "Description": "Webhook endpoint",
        "ExportName": "threatstack-aws-sns-publisher-prime-WebHookEndpoint"
    },
    {
        "OutputKey": "SnsTopicArn",
        "OutputValue": "arn:aws:sns:us-east-1:529602709954:threatstack-aws-sns-publisher-prime-SnsTopic-CQNDFPKNTJGC",
        "Description": "SNS Topic ARN; used by deployed subscribers",
        "ExportName": "threatstack-aws-sns-publisher-prime-SnsTopicArn"
    },
    {
        "OutputKey": "ServiceEndpoint",
        "OutputValue": "https://1f1axqumck.execute-api.us-east-1.amazonaws.com/prime",
        "Description": "URL of the service endpoint"
    },
    {
        "OutputKey": "ServerlessDeploymentBucketName",
        "OutputValue": "threatstack-aws-sns-publ-serverlessdeploymentbuck-wnocrqlbkkye"
    }
]
```

## Development
This repository uses Serverless Framework for managing the development life cycle.  To install Serverless Framework, ensure you have NodeJS and the [NPM](https://www.npmjs.com/get-npm) package manager installed.  Then perform the following.

```
$ npm install -g serverless
$ npm install
```

