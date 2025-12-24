import json
import boto3 
import sys
from datetime import datetime

streamname = 'dea-realtimeproject-stream'
errorbucketname = 'dea-realtimeproject-error-bucket-001'

# Initialize clients
s3_client = boto3.client('s3')
kinesis_client = boto3.client('kinesis')

timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

"""
Lambda function responsible for:
1. Validating incoming JSON payloads
2. Routing invalid records to an S3 error bucket
3. Publishing valid records to Kinesis Data Streams
"""

def lambda_handler(event, context):
    try:
        # Example code logic to process API Gateway event
        # Assuming API Gateway passes JSON data in the event
        data = json.loads(event['body'])

        # Check if 'Id' column exists and is blank    
        if 'Id' in data and (data['Id'] is None or data['Id'] == ''):

            # Include the timestamp in the object key
            object_key = f'error/error_{timestamp}.json'

            # Write data to S3 bucket for error handling
            s3_client.put_object(Bucket=errorbucketname,Key=object_key,Body=json.dumps(data))

            response = {'statusCode': 200,'body': json.dumps({'message': 'Error JSON Data loaded successfully'}),'headers': {'Content-Type': 'application/json'}}

            return response

        else:
            print('Writing to Amazon Kinesis stream')

            kinesis_client.put_record(StreamName=streamname, Data=json.dumps(data), PartitionKey='1' )

            response = {'statusCode': 200,'body': json.dumps({'message': 'JSON Data loaded successfully'}),'headers': {'Content-Type': 'application/json'}}

            return response

    except Exception as e:
        print(f'Error processing event: {e}')

        error_response = {'statusCode': 500,'body': json.dumps(f'Error processing event: {e}'),'headers': {'Content-Type': 'application/json'}}

        return error_response
