import logging
import boto3
import psycopg2
from botocore.exceptions import ClientError
from app.utils import secrets, sns
from app.config import config

secret = secrets.Secrets()
sns = sns.Sns()

class registration:
    # SAVE THE DB CONFIG IN A DICT OBJECT
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.DATABASE_CONFIG = {
            "database": "ecommerce",
            "user": "ecom_user",
            "password": secret.get_secret(secret_name=config.DB_SECRET_NAME),
            "host": config.DB_HOST,
            "port": 5432,
        }

        self.conn = psycopg2.connect(
            dbname=self.DATABASE_CONFIG.get("database"),
            user=self.DATABASE_CONFIG.get("user"),
            password=self.DATABASE_CONFIG.get("password"),
            host=self.DATABASE_CONFIG.get("host"),
            port=self.DATABASE_CONFIG.get("port"),
        )

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
        # CLOSE THE CONNECTION
        self.conn.close()
        sns.publish_to_sns(topic_arn=config.SNS_TOPIC_ARN,message=msg)
        return msg

    def verify_registration(self, email_id):
        self.logger.info("verify_registration begin.. ")
        curr = self.conn.cursor()
        curr.execute(
            f"""
            SELECT email_id FROM customer.cust_registration where
            email_id = {email_id} and is_active = true
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

    
    
