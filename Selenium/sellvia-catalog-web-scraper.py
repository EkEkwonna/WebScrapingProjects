
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd




"Optional Headless bot"
options = Options()
options.headless = True

browser = webdriver.Firefox(options = options)
browser.get('https://sellviacatalog.com/product/1660119')

def extract_images():
    image_array=[]
    first_image = browser.find_element(By.XPATH,"//img[@class='makezoom']").get_attribute('src')
    image_array.append(first_image)
    current_image = 0
    while current_image != first_image:
        browser.find_element(By.XPATH,"//div[@class='slider-next']").click()
        current_image = browser.find_element(By.XPATH,"//img[@class='makezoom']").get_attribute('src')
        if current_image != first_image:
            image_array.append(current_image)
    return image_array

def scrape_elements():
    "Desired Format [product title, description, all images, processing time, all hidden fields] "  
    product_title = browser.find_element(By.XPATH,"//h1[@class='h4']").text
    description = browser.find_element(By.XPATH,"//div[@class='wrap-content']").text
    image_list = extract_images()
    images=' \n'.join(image_list)
    processing_time = browser.find_element(By.XPATH,"//div[@class='single-shipping_title']").text
    row = [product_title,description,images,processing_time]
    return row

data = [scrape_elements()]

df=pd.DataFrame(data,columns=['Title','Description','Images','Processing Time'])

df.to_csv('sellvia-catalog-products.csv',index=False)