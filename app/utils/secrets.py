import boto3
import logging
from botocore.exceptions import ClientError

class Secret():
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_secret(self, secret_name):

            print("current role is:")
            print(boto3.client("sts").get_caller_identity().get("Arn"))

            secret_name = secret_name
            region_name = "us-east-1"

            # Create a Secrets Manager client
            session = boto3.session.Session()
            client = session.client(service_name="secretsmanager", region_name=region_name)

            try:
                get_secret_value_response = client.get_secret_value(SecretId=secret_name)
            except ClientError as e:

                raise e

            secret = get_secret_value_response["SecretString"]

            return secret