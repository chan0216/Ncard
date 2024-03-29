import boto3
import redis
from decouple import config
s3 = boto3.resource(
    service_name='s3',
    region_name='ap-northeast-1',
    aws_access_key_id=config('aws_access_key_id'),
    aws_secret_access_key=config('aws_secret_access_key')
)
redis = redis.Redis(config('redis_host'), port=6379)
