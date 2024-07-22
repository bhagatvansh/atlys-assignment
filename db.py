import mysql.connector
from dotenv import load_dotenv
import os
import datetime

def connect_to_db():

    load_dotenv()

# Database configurations from environment variables
    MYSQL_CONFIG = {
        'user': os.getenv('MYSQL_USER'),
        'password': os.getenv('MYSQL_PASSWORD'),
        'host': os.getenv('MYSQL_HOST'),
        'database': os.getenv('MYSQL_DATABASE')
    }
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
    except:
        print("Unable to connect to DB.")
    
    return conn
    


def insert_products(conn, products):
    try:
        
        cursor = conn.cursor()

        for product in products:
            cursor.execute(
                "INSERT INTO product_details (product_title, product_price, path_to_image, created_at) VALUES (%s, %s, %s, %s)",
                (product['name'], product['price'], product['image_url'], datetime.datetime.now())
            )

        conn.commit()
        cursor.close()
        conn.close()

    except mysql.connector.Error as e:
        print(f"Error saving to DB: {e}")

def update_products(conn, products):
    try:
        
        cursor = conn.cursor()

        for product in products:
            cursor.execute(
                "UPDATE product_details SET product_price = %s where product_title = %s",
                (product['price'], product['name'])
            )

        conn.commit()
        cursor.close()
        conn.close()

    except mysql.connector.Error as e:
        print(f"Error updating to DB: {e}")