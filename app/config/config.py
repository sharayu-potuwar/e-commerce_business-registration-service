import os

APP_ENV = os.environ["ENV_CONFIG"]

if APP_ENV == "dev":
    DB_SECRET_NAME = "dev_ecom_db_secret"
    DB_HOST = "dev-e-commerce.c3m660qam72y.us-east-1.rds.amazonaws.com"
    SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:211125373436:dev_ecom-user-updates-topic"
else:
    DB_SECRET_NAME = "prod_ecom_db_secret"
    DB_HOST = "prod-e-commerce.c3m660qam72y.us-east-1.rds.amazonaws.com"
    SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:211125373436:prod_ecom-user-updates-topic"