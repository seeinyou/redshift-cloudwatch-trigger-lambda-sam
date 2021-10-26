
# Redshift Cluster Operation Lambda Functions

# Introduction  

In many use cases, the OLTP workloads on Redshift clusters usually run a few times a week and could finish in a short period of time, so it could be much more economical to run the workloads on larger clusters so that they could finish in a shorter period of time and Redshift clusters could be paused for the cost saving propose.

This project is developed to automate Redshift cluster operations in a cost effective way.

The project is built-on AWS Serverless Application Model (**SAM**), which is a convenient tool to manage Serverless applications in AWS. Please check the [SAM Developer Guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html).

# Files

- src - Code for the application's Lambda function.
- events - Invocation events that you can use to invoke the function.
- tests - Unit tests for the application code.
- template.yaml - A template that defines the application's AWS resources.

The application uses several AWS resources, including **Lambda functions** and a **Amazon SNS topic**. These resources are defined in the `template.yaml` file in this project. You can update the template to add AWS resources through the same deployment process that updates your application code.

## Lambda functions

## src
- pause.py - Extract information from SNS messages and execute Redshift cluster **pause** action to pause a Redshift cluster.

## SAM Template
- Resources
  - An Amazon SNS topic
  - The permission to trigger Lambda functions for the SNS topic
  - Lambda function **RedshiftOpsPauseClusterFunction** for the **pause** action

# Deployment

## Prerequisites
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
- An Amazon S3 bucket
- Amazon IAM users and roles
- Python 3.8

## Amzon IAM users and roles
- An IAM user for the SAM CLI to call relevant AWS services, including CloudFormation and S3.
- An IAM role for Lambda functions to receive SNS messages and call Redshift cluster operation APIs such as describe-clusters and pause-cluster, etc.

## Deploy the application using SAM
- Create a package
  > sam package --template-file template.yaml --output-template-file packaged.yaml --s3-bucket [S3-bucket-name-for-your-code]
  
- Deploy the project
  > sam deploy --template-file /path/to/packaged.yaml --stack-name [project-name] --capabilities CAPABILITY_IAM

## Configure Redshift cluster CloudWatch alarm
- Create a CloudWatch alarm to monitor the CPU utilization of a Redshift cluster.
- Set the alarm threshold to preferred values. For example 5 for 1 minutes.
- Configure an action to send a notification to an Amazon SNS topic, which should be created in the SAM template.

## Conclusion
Now, if a Redshift cluster CPU utilization is lower than the cluster alarm threshold for configured minutes, a CloudWatch alarm will be triggered and a notification will be sent to the SNS topic. Then, the SNS topic will trigger a Lambda function to execute a Redshift cluster operation such as pause, etc.