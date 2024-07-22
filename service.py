from db import insert_products,connect_to_db,update_products
from cache import save_to_cache,read_from_cache,connect_to_cache,update_cache
from notification_context import NotificationContext
from sms import SMSNotification

cache_conn = None
db_conn = None

def segregate_products(products):
    products_to_be_inserted = []
    products_to_be_updated = []
    for product in products:
            if cache_conn is None: 
                connect_to_cache()
            cached_product = read_from_cache(cache_conn, product['product_title'])
            if cached_product and cached_product['product_price'] != product['product_price']:
                # Update only if the price has changed
                products_to_be_updated.append(product)
            elif not cached_product:
                # If the product is not in cache, save it
                products_to_be_inserted.append(product)
    if len(products_to_be_inserted) > 0:
        insert_products(products_to_be_inserted)
    if len(products_to_be_updated) > 0:
         update_products(products_to_be_updated)

def update_products(products):
    if db_conn is None:
        connect_to_db()
        update_products(products=products)
    else:
        update_products(products=products)
    
    if cache_conn is None:
         connect_to_cache()
         update_cache(products=products)
    else:
         update_cache(products=products)

    NotificationContext.notify(products=products)

def insert_products(products):
    if db_conn is None:
        connect_to_db()
        insert_products(products=products)
    else:
        insert_products(products=products)
    
    if cache_conn is None:
         connect_to_cache()
         save_to_cache(products=products)
    else:
         save_to_cache(products=products)

    NotificationContext.notify(products=products)

NotificationContext.set_strategy(SMSNotification(
    sms_gateway='your_sms_gateway',
    auth_token='your_auth_token',
    from_number='your_phone_number'
),SMSNotification)