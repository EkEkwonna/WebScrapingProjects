
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd

browser = webdriver.Firefox()
data = []

def extract_images():
    image_array=[]
    first_image = browser.find_element(By.XPATH,"//img[@class='makezoom']").get_attribute('data-zoom-image')
    image_array.append(first_image)
    current_image = 0
    while current_image != first_image:
        browser.find_element(By.XPATH,"//div[@class='slider-next']").click()
        current_image = browser.find_element(By.XPATH,"//img[@class='makezoom']").get_attribute('src')
        if current_image != first_image:
            image_array.append(current_image)
    return image_array

def extract_hidden_fields():
    output = []
    hidden_fields_dictionary = {}
    hidden_fields = [(field.get_attribute('name'),field.get_attribute('value')) for field in browser.find_elements(By.XPATH,"//input[@type='hidden']")]
    
    for (key,value) in hidden_fields:
        hidden_fields_dictionary[str(key)]=value

    "maximum number of hidden fields is 24 with the following keys"
    keys = ['post_id','currency','_price','_price_nc','_save','_save_nc','stock','savePercent','_salePrice','_salePrice_nc',
     'price','salePrice','save','single_shipping_price','currency_shipping','variation_default','shipping','sku-meta','sku-meta-set[]']
    for key in keys:
        if key in hidden_fields_dictionary.keys():
            output.append(hidden_fields_dictionary[key])
        else:
            output.append('')
    return output

def extract_all_details():
    WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH,"//h1[@class='h4']")))
    WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH,"//span[@class = 'number']")))
    product_title = browser.find_element(By.XPATH,"//h1[@class='h4']").text
    display_price = float(browser.find_element(By.XPATH,"//span[@class = 'number']").text.split('$')[1])
    retail_price = float(browser.find_element(By.XPATH,"//div[@class = 'product-single-retail']").text.split('$')[1])

    description = browser.find_element(By.XPATH,"//div[@class='wrap-content']").text
    image_list = extract_images()
    processing_time = browser.find_element(By.XPATH,"//div[@class='single-shipping_title']").text.split(': ')[1]
    shipping_and_handling = float(browser.find_element(By.XPATH,"//span[@class = 'js-sku-shipping-price']").text.split('$')[1])
        
    "Checking Stock Levels"
    if browser.find_element(By.XPATH,"//div[@class='stock']").text == 'In Stock':
        stock = 'Yes'
    else:
        stock = 'No'

    "Identifying Options"
    [Type,Size,Color] = ['Type','Size','Color']
    feature_options = [Type,Size,Color]
    for i in range(len(feature_options)):
        if len(browser.find_elements(By.XPATH,f"//div[@class='name' and (contains(text(),'{feature_options[i]}'))]")) == 1:
            element_containing_option=browser.find_element(By.XPATH,f"//div[@class='name' and contains(text(),'{feature_options[i]}')]")
            feature_options[i] = element_containing_option.find_element(By.XPATH,".//span[@style = 'margin: 0px 0px 0px 5px;']").text
        else:
            feature_options[i] = ''

    "We're assuming all prices are considered in USD ($) for the entire website"
    row = [product_title,description,display_price,retail_price,processing_time,shipping_and_handling,feature_options[0],feature_options[1],feature_options[2]]
    row +=image_list


    for i in range(15 - len(image_list)):
        row.append('')
    row += [processing_time,stock]
        
    hidden_fields = extract_hidden_fields()
    row += hidden_fields
    return row

def scrape_elements(product_code):
    browser.get(f'https://sellviacatalog.com/product/{str(product_code)}')
    print('Exctracting for product:',str(product_code))
    available_options = [item.text for item in browser.find_elements(By.XPATH,"//span[contains(@class,'js-sku-set meta-item meta-item-text is-not-empty')]")]
    if len(available_options) <=1 :
        data_entry = extract_all_details()
        data.append(data_entry)
    else:
        for option in available_options:
            button = browser.find_element(By.XPATH,f"//span[contains(@data-title,'{option}')]").click()
            data_entry = extract_all_details()
            data.append(data_entry)
        return
    

for item in range(1660119,1660110,-1):
    scrape_elements(item)

df=pd.DataFrame(data,columns=['Title','Description','Display Price USD($)','Retail Price USD($)','Processing Time','Shipping and Handling USD ($)','Type','Size','Color',
                              'Image_1','Image_2','Image_3','Image_4','Image_5','Image_6','Image_7','Image_8','Image_9','Image_10',
                              'Image_11','Image_12','Image_13','Image_14','Image_15',
                              'Processing Time','In Stock',
                              #hidden_fields
                              'post_id','currency','_price','_price_nc','_save','_save_nc','stock','savePercent','_salePrice','_salePrice_nc',
                                'price','salePrice','save','single_shipping_price','currency_shipping','variation_default','shipping','sku-meta','sku-meta-set[]'])

df.to_csv('sellvia-catalog-products.csv',index=False)
print('CSV created under sellvia-catalog-products.csv')

