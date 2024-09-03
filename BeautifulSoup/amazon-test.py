from bs4 import BeautifulSoup
import requests
import pandas as pd
import random 
import time
import json 
import re


class Amazon_product:
  def __init__(self,ASIN_VALUE):
    response = requests.get(f'https://amazon.com/dp/{ASIN_VALUE}',headers= custom_headers)
    soup = BeautifulSoup(response.text,'lxml')
    self.ASIN = ASIN_VALUE
    self.Title =  soup.select_one('#productTitle').text.strip()
    self.Description = soup.find('ul',class_='a-unordered-list a-vertical a-spacing-mini').text.strip()
    self.DisplayPrice = ''
    self.FastestDeliveryDate = ''
    
    if soup.find('div',class_='a-section a-spacing-none a-padding-none') != None :
       if soup.find('div',class_='a-section a-spacing-none a-padding-none').find('span',class_='a-price-whole') != None:
            self.DisplayPrice = soup.find('div',class_='a-section a-spacing-none a-padding-none').find('span',class_='a-price-whole').text.strip() + soup.find('div',class_='a-section a-spacing-none a-padding-none').find('span',class_='a-price-fraction').text.strip()
       
    
    if soup.find('div',class_='a-section a-spacing-none a-padding-none') !=None :
      #  print('===============TRYING TO LOCATE SHIPPING CHARGE AND FASTEST DELIVERY DATE')
      #  print(soup.find('div',class_='a-section a-spacing-none a-padding-none'))
       self.ShippingCharge = soup.find('div',class_='a-section a-spacing-none a-padding-none').find('span',class_='a-size-base a-color-secondary').text.strip()
       self.FastestDeliveryDate = soup.find('div',class_='a-section a-spacing-none a-padding-none').find('span',class_='a-text-bold').text.strip()
      #  print(self.FastestDeliveryDate,self.ShippingCharge)
    else:
       self.ShippingCharge = soup.find('span',class_='a-color-price').text.strip()
       self.FastestDeliveryDate = 'N/A'
    
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
    self.image_list = list(imgs_dict.keys())
    self.Image = dict()
    image_array = ['Image1','Image2','Image3','Image4','Image5','Image6','Image7','Image8','Image9','Image10']
    for i in range(len(self.image_list)):
       self.Image[image_array[i]] = self.image_list[i]
    
    for j in range(9,len(self.image_list)-1,-1):
       self.Image[image_array[j]] = ''
    
    available_options= [list_index['data-csa-c-item-id'] for list_index in soup.select('li[data-csa-c-item-id]') 
                        if (list_index['data-csa-c-item-id'] not in ASIN_LIST and list_index['data-csa-c-item-id'] != '' and list_index['data-csa-c-item-id'] not in ALL_EXPLORED_ASINS)]
    
    global ASIN_LIST
    ASIN_LIST+=available_options

  def row(self):
     print([self.ASIN,self.Title,self.Description,self.DisplayPrice,self.FastestDeliveryDate,self.ShippingCharge,self.Stock,self.Color, self.Size ,self.Style ,self.Image['Image1'],self.Image['Image2'],self.Image['Image3'],self.Image['Image4'],self.Image['Image5'],self.Image['Image6'],self.Image['Image7'],self.Image['Image8'],self.Image['Image9'],self.Image['Image10']])
     return [self.ASIN,self.Title,self.Description,self.DisplayPrice,self.FastestDeliveryDate,self.ShippingCharge,self.Stock,self.Color, self.Size ,self.Style ,self.Image['Image1'],self.Image['Image2'],self.Image['Image3'],self.Image['Image4'],self.Image['Image5'],self.Image['Image6'],self.Image['Image7'],self.Image['Image8'],self.Image['Image9'],self.Image['Image10']]
    


custom_headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
                  'Accept-Language':'en-GB,en-US;q=0.9,en;q=0.8'}

ASIN_LIST = [
   #  'B0C33B6H4Z',
    'B0BTK1C533'
    # 'B07MXF4G8K','B08BXBCNMQ','B07BRK1PW4','B07GDLCQXV','B07XSCCZYG','B01DJLKZBA','B07XSCD2R4','B08MVFKGJM','B0032JUOU2','B0D7M3ZJ1Z','B0BMXYPFTK','B0CN6SLBGD'
    ]

data = []
ALL_EXPLORED_ASINS = []
for ASIN_VALUE in ASIN_LIST:
    if ASIN_VALUE not in ALL_EXPLORED_ASINS:
       item = Amazon_product(ASIN_VALUE)
       data.append(item.row())
       ALL_EXPLORED_ASINS.append(ASIN_VALUE)

df=pd.DataFrame(data,columns=['ASIN','Title','Description','Display Price','Fastest Delivery Date','Shipping Charge','Stock','Color','Size','Style',
                              'Image_1','Image_2','Image_3','Image_4','Image_5','Image_6','Image_7','Image_8','Image_9','Image10'])
df.to_csv('amazon-test.csv',index=False)




       



