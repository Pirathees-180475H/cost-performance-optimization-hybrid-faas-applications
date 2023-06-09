import boto3
import time

def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    # Download a 25MB file from S3
    with open('/tmp/25MB', 'wb') as data:
        s3_client.download_fileobj('serverlessappperfopt-network-intensive-source-bucket', '25MB', data)
    time.sleep(0.1)
    #Delete the file on S3
    s3_client.delete_object(
        Bucket='serverlessappperfopt-network-intensive-source-bucket',
        Key='25MB'
    )
    time.sleep(0.1)
    # Upload a 25MB file to S3
    with open('/tmp/25MB', 'rb') as data:
        s3_client.upload_fileobj(data, 'serverlessappperfopt-network-intensive-source-bucket', '25MB')
    return {
        'statusCode': 200,
        'body': "'f4'"
    }