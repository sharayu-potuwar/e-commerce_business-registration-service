import boto3


class Sns:
    def __init__(self):
        self.client = boto3.client("sns", region_name="us-east-1")

    def publish_to_sns(self, topic_arn, message):
        response = self.client.publish(
            TopicArn=topic_arn,
            Message=message,
        )
        return response
