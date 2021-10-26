import json
import os
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    statusCode = 400
    return_msg = ''

    print('### EVENT:', event)

    # Extract Redshift cluster information from the event variable
    sns_msg = json.loads(event['Records'][0]['Sns']['Message'])
    redshift_cluster_identifier = sns_msg['Trigger']['Dimensions'][0]['value']
    
    # DEBUG
    # print('MSG: ', sns_msg)
    print('### CLUSTER IDENTIFIER:', redshift_cluster_identifier)
    
    if redshift_cluster_identifier:

        # Get the current cluster status
        try:
            client = boto3.client('redshift')
            describe_response = client.describe_clusters(ClusterIdentifier=redshift_cluster_identifier)
            print('### CLUSTER INFO:', describe_response)

            if describe_response['Clusters'][0]['ClusterIdentifier'] == redshift_cluster_identifier:
                
                # Only try to pause the Redshift cluster when the cluster status is "Available"
                if describe_response['Clusters'][0]['ClusterStatus'] == 'available':

                    try:
                        pause_response = client.pause_cluster(ClusterIdentifier=redshift_cluster_identifier)
                        print('### REDSHIFT CLUSTER PAUSE RESULT:', pause_response)
                        
                        # Set successful return values
                        statusCode = 200
                        return_msg = 'The Redshift cluster is pausing.'
                        
                    except Exception as e:
                        print('Pause Redshift cluster failed!', e)
                        print('Error: ', e.response['Error']['Code'])

                else:
                    return_msg = 'The Redshift cluster is not in the Available status!'

            else:
                return_msg = 'Could not find the correct Redshift cluster!'

        except Exception as e:
            print('Describe Redshift cluster failed!', e)
            print('Error: ', e.response['Error']['Code'])

            statusCode = 400

    # Save logs
    print('### RESULT:', return_msg)

    # Output and exit
    return  {
        "statusCode": statusCode,
        "body": return_msg
    }
