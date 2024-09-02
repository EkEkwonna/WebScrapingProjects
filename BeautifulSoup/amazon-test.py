from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import random 
import time


class Amazon_product:
  def __init__(self,ASIN_VALUE,attribute_dimensions):
    response = requests.get(f'https://amazon.com/dp/{ASIN_VALUE}',headers= custom_headers)
    soup = BeautifulSoup(response.text,'lxml')
    print(response.status_code)
    self.ASIN = ASIN_VALUE
    self.Title =  soup.select_one('#productTitle').text.strip()
    self.Description = soup.find('ul',class_='a-unordered-list a-vertical a-spacing-mini').text
    self.DisplayPrice = ''
    self.FastedDeliveryDate = ''
    if soup.find('div',class_='a-section a-spacing-none a-padding-none') !=None:
       self.ShippingCharge = soup.find('div',class_='a-section a-spacing-none a-padding-none').find('span',class_='a-size-base a-color-secondary').text
    else:
       self.ShippingCharge = soup.find('div',class_='a-section a-spacing-none a-padding-none').find('span',class_ = 'a-color-error').text
    self.Stock = soup.select_one('#availability')
    [self.Color]
    self.Color = ''
    self.Size = ''
    self.Style = ''
    self.Images = collect_images()
    self.row = [self.ASIN,self.Title,self.Description,self.DisplayPrice,self.FastedDeliveryDate,
                self.ShippingCharge,self.Stock,self.Color, self.Size ,self.Style ,self.Images]
    
    print([self.ASIN,self.Title,self.Description,self.DisplayPrice,self.FastedDeliveryDate,
           self.ShippingCharge ,self.Stock,self.Color, self.Size ,self.Style ,self.Images])

  def collect_images():
    output_array = []
    return output_array

custom_headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
                  'Accept-Language':'en-GB,en-US;q=0.9,en;q=0.8'}

ASIN_LIST = [
    'B0C33B6H4Z'
    # 'B07MXF4G8K','B08BXBCNMQ','B07BRK1PW4','B07GDLCQXV','B07XSCCZYG','B01DJLKZBA','B07XSCD2R4','B08MVFKGJM','B0032JUOU2','B0D7M3ZJ1Z','B0BMXYPFTK','B0CN6SLBGD'
    ]

for ASIN_VALUE in ASIN_LIST: 
    item = Amazon_product(ASIN_VALUE)



