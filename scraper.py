from pydantic import BaseModel
from typing import Optional,List
import requests
from bs4 import BeautifulSoup
import time
import os

class ScrapeRequest(BaseModel):
    base_url:str
    page_limit:Optional[int] = None
    proxy_string:Optional[str] = None
    retry_limit:Optional[int] = None
    delay:Optional[int] = None

class Product(BaseModel):
    product_title:str
    product_price:Optional[str] = None
    path_to_image:Optional[str] = None

def scrape_catalogue(base_url : str, page_limit: Optional[int], proxy_string: Optional[str], retry_limit : Optional[int], delay: Optional[int]) -> List[Product]:
    products = []
    if page_limit is None:
        page_limit = 1
     
    if retry_limit is None:
        retry_limit = 3

    if delay is None:
        delay = 10

    error_threshold = 0
    
    proxies = {"http":proxy_string, "https":proxy_string} if proxy_string else None
    
    page_number = 1

    while True and error_threshold <= retry_limit:
        if page_limit and page_number > page_limit:
            break
        url = base_url
        if page_number > 1:
            url = f"{base_url}/page/{page_number}"

        if proxies is not None:
            response = requests.get(url, proxies=proxies)
        else:
            response = requests.get(url)
        if response.status_code != 200:
            error_threshold += 1
            time.sleep(delay)

        soup = BeautifulSoup(response.text, 'html.parser')

        proudct_grid = soup.find('ul',class_='products columns-4')
        product_items = proudct_grid.find_all('li')
        
        if not product_items:
            break

        for idx ,item in enumerate(product_items):
            if(idx == 24):
                break
            
            name_tag = item.find('h2', class_='woo-loop-product__title')
            try:
                name = name_tag.get_text(strip=True)
            except Exception as e:
                name = 'Could not be parsed'
            price_tag = item.find('span',class_='woocommerce-Price-amount amount')
            try:
                price = price_tag.get_text(strip=True)
            except Exception as e:
                price = '0.00'
            image_tag = item.find('img',class_='attachment-woocommerce_thumbnail size-woocommerce_thumbnail')
            try:
                image_url = image_tag['data-lazy-srcset']
            except Exception as e:
                try:
                    image_url = image_tag['data-lazy-src']
                except Exception as e:
                    print(image_tag)
            image_url = image_url.split(" ")[0]
            image_dir = save_image(image_url=image_url,product_title=name,images_dir='C://Users://Admin/atlys/')
            products.append(Product(product_title=name, product_price=price,path_to_image=image_dir))

        page_number += 1

    return products

def save_image(image_url: str, product_title: str, images_dir: str) -> str:
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
    
    image_filename = f"{images_dir}/{product_title}.jpg"
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()  # Raise an error for HTTP request issues
        with open(image_filename, 'wb') as out_file:
            for chunk in response.iter_content(chunk_size=8192):
                out_file.write(chunk)
        return image_filename
    except requests.RequestException as e:
        print(f"Error saving image {image_url}: {e}")
        return None
