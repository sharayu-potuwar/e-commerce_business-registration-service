import logging
import boto3
import psycopg2
from botocore.exceptions import ClientError
from app.utils import secrets, sns, db_connection
from app.config import config

secret = secrets.Secret()
sns = sns.Sns()
db_connection = db_connection.DbConnection()

class registration:
    # SAVE THE DB CONFIG IN A DICT OBJECT
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def insert_customer(self, dicobj):
        self.logger.info("insert_customer begin.. ")
        conn = db_connection.get_connection()
        curr = conn.cursor()

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
        conn.commit()
        # CLOSE THE CONNECTION
        conn.close()
        sns.publish_to_sns(topic_arn=config.SNS_TOPIC_ARN,message=msg)
        return msg

    def verify_registration(self, email_id):
        self.logger.info("verify_registration begin.. ")
        conn = db_connection.get_connection()
        curr = conn.cursor()

        curr.execute(
            f"""
            SELECT email_id FROM customer.cust_registration where
            email_id = "{email_id}" and is_active = true
            """
        )
        result = curr.fetchone()

        if result[0] is None:
            msg = "User does not exist"
        else:
            msg = "User exist.You may login"
        # COMMIT THE ABOVE REQUESTS
        conn.commit()

        # CLOSE THE CONNECTION
        conn.close()

        return msg

    
    
