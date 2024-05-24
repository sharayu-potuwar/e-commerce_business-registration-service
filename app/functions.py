import json
import logging
from datetime import datetime

import boto3
import psycopg2
from botocore.exceptions import ClientError


class registration:
    # SAVE THE DB CONFIG IN A DICT OBJECT
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.DATABASE_CONFIG = {
            "database": "ecommerce",
            "user": "ecom_user",
            "password": self.get_secret(),
            "host": "e-commerce.c3m660qam72y.us-east-1.rds.amazonaws.com",
            "port": 5432,
        }

        # def get_connection(self):
        # Connect to your postgres DB
        # return
        self.conn = psycopg2.connect(
            dbname=self.DATABASE_CONFIG.get("database"),
            user=self.DATABASE_CONFIG.get("user"),
            password=self.DATABASE_CONFIG.get("password"),
            host=self.DATABASE_CONFIG.get("host"),
            port=self.DATABASE_CONFIG.get("port"),
        )
        self.client = boto3.client("sns", region_name="us-east-1")

    def insert_customer(self, dicobj):
        self.logger.info("insert_customer begin.. ")
        curr = self.conn.cursor()

        # EXECUTE THE INSERT QUERY
        curr.execute(
            f""" 
            INSERT INTO 
                customer.cust_registration(first_name,last_name,
                    email_id,
                    phone,
                    city,postacode,province)
            VALUES 
                ('{dicobj.get('first_name')}','{dicobj.get('last_name')}',
                '{dicobj.get('email_id')}',
                '{dicobj.get('phone')}','{dicobj.get('city')}',
                '{dicobj.get('postalcode')}','{dicobj.get('province')}'
                ) 
        """
        )
        if curr.statusmessage is None:
            msg = "registration failed"
        else:
            msg = "registration is successfull"

        # COMMIT THE ABOVE REQUESTS
        self.conn.commit()

        self.publish_to_sns(dicobj.get("email_id"))
        # CLOSE THE CONNECTION
        self.conn.close()

        return msg

    def verify_registration(self, email_ID):
        self.logger.info("verify_registration begin.. ")
        curr = self.conn.cursor()
        curr.execute(
            """
                        SELECT email_id FROM customer.cust_registration where email_id = email_ID and is_active = true
                    """
        )
        result = curr.fetchone()

        if result[0] is None:
            msg = "User does not exist"
        else:
            msg = "User exist.You may login"
        # COMMIT THE ABOVE REQUESTS
        self.conn.commit()

        # CLOSE THE CONNECTION
        self.conn.close()

        return msg

    def publish_to_sns(self, email_ID):
        self.logger.info("publish_to_sns begin.. ")
        response = self.client.publish(
            TopicArn="arn:aws:sns:us-east-1:211125373436:ecom-user-updates-topic",
            Message="Test message",
        )
        print("Message published")
        return response

    def get_secret(self):

        print("current role is:")
        print(boto3.client("sts").get_caller_identity().get("Arn"))

        secret_name = "dev_ecom_secretmanager"
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
