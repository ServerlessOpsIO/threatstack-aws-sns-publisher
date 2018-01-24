# threatstack-aws-sns-publisher

[![Build Status](https://travis-ci.org/ServerlessOpsIO/threatstack-aws-sns-publisher.svg?branch=master)](https://travis-ci.org/ServerlessOpsIO/threatstack-aws-sns-publisher) [![License](https://img.shields.io/badge/License-BSD%202--Clause-orange.svg)](https://opensource.org/licenses/BSD-2-Clause) 

Receives webhooks from Threat Stack and publishes alert details to an SNS topic.  Subsribe additional services to the SNS topic to aggregate alert data to multiple services.

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

## Development
This repository uses Serverless Framework for managing the development life cycle.  To install Serverless Framework, ensure you have NodeJS and the [NPM](https://www.npmjs.com/get-npm) package manager installed.  Then perform the following.

```
$ npm install -g serverless
$ npm install
```

