import json
import boto3
import base64
import os
import gzip
from io import BytesIO
from datetime import datetime

s3 = boto3.client('s3')
bucket_name = os.environ['S3_BUCKET']

def lambda_handler(event, context):
    compressed_batch = BytesIO()

    with gzip.GzipFile(fileobj=compressed_batch, mode='w') as gz:
        for record in event['Records']:
            try:
                raw_data = base64.b64decode(record['kinesis']['data'])
                log_event = json.loads(raw_data)

                # Append each log as JSON line
                gz.write((json.dumps(log_event) + '\n').encode('utf-8'))

            except Exception as e:
                print(f"Error processing record: {e}")
                continue

    compressed_batch.seek(0)

    now = datetime.utcnow()
    key_prefix = f"logs/{now.year}/{now.month:02d}/{now.day:02d}/{now.hour:02d}/"
    object_key = key_prefix + f"log_batch_{context.aws_request_id}.json.gz"

    try:
        s3.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=compressed_batch.read(),
            ContentEncoding='gzip',
            ContentType='application/json'
        )
        return {
            "status": "success",
            "s3_key": object_key,
            "records_processed": len(event['Records'])
        }
    except Exception as e:
        print(f"Failed to upload to S3: {e}")
        raise
