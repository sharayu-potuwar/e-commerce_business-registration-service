import json
import psycopg2
from datetime import datetime

class registration():
    # SAVE THE DB CONFIG IN A DICT OBJECT 
    DATABASE_CONFIG = { 
        "database": "ecommerce", 
        "user": "ecom_user", 
        "password": "zPFJ6Pl25lZAzyE7jMytDIWUcpmqr5Ul", 
        "host": "e-commerce.c3m660qam72y.us-east-1.rds.amazonaws.com", 
        "port":  5432, 
    } 

    # def get_connection(self):
    # Connect to your postgres DB
    # return 
    conn=psycopg2.connect(dbname=DATABASE_CONFIG.get('database') ,
                            user=DATABASE_CONFIG.get('user'),
                            password=DATABASE_CONFIG.get('password'),
                            host=DATABASE_CONFIG.get('host'), 
                            port=DATABASE_CONFIG.get('port')) 

    def insert_customer(self,dicobj):
        curr =self.conn.cursor()
        
        # EXECUTE THE INSERT QUERY 
        curr.execute(f''' 
            INSERT INTO 
                customer.cust_registration(first_name,last_name,
                    email_id,
                    phone,
                    city,postacode,province)
            VALUES 
                ('{dicobj.get('first_name')}','{dicobj.get('last_name')}',
                '{dicobj.get('email_id')}',
                '{dicobj.get('phone')}','{dicobj.get('city')}',
                '{dicobj.get('postacode')}','{dicobj.get('province')}'
                ) 
        ''') 
        if curr.statusmessage is None:
            msg="registration failed"
        else:
            msg="registration is successfull"
         
        # COMMIT THE ABOVE REQUESTS 
        self.conn.commit() 
    
        # CLOSE THE CONNECTION 
        self.conn.close()

        return msg

    def verify_registration(self,email_ID):
        curr = self.conn.cursor()
        curr.execute('''
                        SELECT email_id FROM customer.cust_registration where email_id = email_ID and is_active = true
                    ''')
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

# def main():
#     Cust_registration = registration()
    
# main()
