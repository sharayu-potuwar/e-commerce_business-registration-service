import boto3
import json

class Sns:
    def __init__(self):
        self.client = boto3.client("sns", region_name="us-east-1")

    def publish_to_sns(self, topic_arn, obj):
        response = self.client.publish(
            TopicArn=topic_arn,
            Message=json.dumps(obj),
        )
        return response
    

