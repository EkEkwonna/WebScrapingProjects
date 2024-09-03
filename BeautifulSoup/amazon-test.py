from bs4 import BeautifulSoup
import requests
import pandas as pd
import random 
import time
import json 


class Amazon_product:
  def __init__(self,ASIN_VALUE):
    response = requests.get(f'https://amazon.com/dp/{ASIN_VALUE}',headers= custom_headers)
    soup = BeautifulSoup(response.text,'lxml')
    print(response.status_code)
    self.ASIN = ASIN_VALUE
    self.Title =  soup.select_one('#productTitle').text.strip()
    self.Description = soup.find('ul',class_='a-unordered-list a-vertical a-spacing-mini').text.strip()
    self.DisplayPrice = ''
    self.FastedDeliveryDate = ''
    
    if soup.find('div',class_='a-section a-spacing-none a-padding-none') != None :
       if soup.find('div',class_='a-section a-spacing-none a-padding-none').find('span',class_='a-price-whole') != None:
            self.DisplayPrice = soup.find('div',class_='a-section a-spacing-none a-padding-none').find('span',class_='a-price-whole').text.strip() + '.' + soup.find('div',class_='a-section a-spacing-none a-padding-none').find('span',class_='a-price-fraction')
       
    
    if soup.find('div',class_='a-section a-spacing-none a-padding-none') !=None:
       self.ShippingCharge = soup.find('div',class_='a-section a-spacing-none a-padding-none').find('span',class_='a-size-base a-color-secondary').text.strip()
    else:
       self.ShippingCharge = soup.find('span',class_='a-color-price').text.strip()
    
    self.Stock = soup.select_one('#availability').text.strip()
    [self.Color,self.Size ,self.Style] = ['','','']

    for attribute in ['size','color','style']:
       if soup.select_one(f'#variation_{attribute}_name') != None:
            if attribute == 'size':
                self.Size = soup.select_one(f'#variation_{attribute}_name').find('span',class_='selection').text.strip()
            if attribute == 'color':
                self.Color = soup.select_one(f'#variation_{attribute}_name').find('span',class_='selection').text.strip()
            if attribute == 'style':
                self.Style = soup.select_one(f'#variation_{attribute}_name').find('span',class_='selection').text.strip()

    "Extracting Images"
    img_div = soup.find(id="imgTagWrapperId")
    imgs_str = img_div.img.get('data-a-dynamic-image')  
    imgs_dict = json.loads(imgs_str)
    self.Images = list(imgs_dict.keys())
    
  def row(self):
     print([self.ASIN,self.Title,self.Description,self.DisplayPrice,self.FastedDeliveryDate,self.ShippingCharge,self.Stock,self.Color, self.Size ,self.Style ,self.Images])
     return [self.ASIN,self.Title,self.Description,self.DisplayPrice,self.FastedDeliveryDate,self.ShippingCharge,self.Stock,self.Color, self.Size ,self.Style ,self.Images]
    

    
custom_headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
                  'Accept-Language':'en-GB,en-US;q=0.9,en;q=0.8'}

ASIN_LIST = [
    'B0C33B6H4Z'
    # 'B07MXF4G8K','B08BXBCNMQ','B07BRK1PW4','B07GDLCQXV','B07XSCCZYG','B01DJLKZBA','B07XSCD2R4','B08MVFKGJM','B0032JUOU2','B0D7M3ZJ1Z','B0BMXYPFTK','B0CN6SLBGD'
    ]

for ASIN_VALUE in ASIN_LIST: 
    "THE HTML UPDATES the list items with different ASIN codes for all available options"
    "All you have to do is find all combinations and then find elements once they are displayed and select the ones that are displayed"
    item = Amazon_product(ASIN_VALUE)
    item.row()



