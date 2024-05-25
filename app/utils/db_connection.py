import psycopg2
from app.utils import secrets
from app.config import config


class DbConnection():
    def __init__(self):
        secret = secrets.Secret()
        self.DATABASE_CONFIG = {
                    "database": "ecommerce",
                    "user": "ecom_user",
                    "password": secret.get_secret(secret_name=config.DB_SECRET_NAME),
                    "host": config.DB_HOST,
                    "port": 5432,
                }

    def get_connection(self):
        conn = psycopg2.connect(
            dbname=self.DATABASE_CONFIG.get("database"),
            user=self.DATABASE_CONFIG.get("user"),
            password=self.DATABASE_CONFIG.get("password"),
            host=self.DATABASE_CONFIG.get("host"),
            port=self.DATABASE_CONFIG.get("port"),
        )

        return conn
