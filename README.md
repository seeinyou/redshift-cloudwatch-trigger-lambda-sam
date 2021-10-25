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

