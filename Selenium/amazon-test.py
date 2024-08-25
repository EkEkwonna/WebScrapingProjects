
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd

options = Options()
options.headless = False
browser = webdriver.Firefox(options=options)
browser.fullscreen_window()
browser.execute_script("document.body.style.zoom='5%'")
data = []

def check_product(element_type,field,attribute_detail):
    WebDriverWait(browser,100000).until(EC.presence_of_element_located((By.XPATH,f"//{element_type}[@{field} = '{attribute_detail}']")))
    if browser.find_elements(By.XPATH,f"//{element_type}[@{field} = '{attribute_detail}']") != []:
        WebDriverWait(browser,100000).until(EC.presence_of_element_located((By.XPATH,f"//{element_type}[@{field} = '{attribute_detail}']")))
        output = browser.find_element(By.XPATH,f"//{element_type}[@{field} = '{attribute_detail}']").text 
        return output
    else:
        return ''
    
def extract_images():
    # left_container = browser.find_element(By.XPATH,"//ul[@class = 'a-unordered-list a-nostyle a-button-list a-vertical a-spacing-top-micro regularAltImageViewLayout']")
    image_array = [image.get_attribute('src') for image in browser.find_elements(By.XPATH,"//ul[@class = 'a-unordered-list a-nostyle a-button-list a-vertical a-spacing-top-micro regularAltImageViewLayout']//img")]
    return image_array


def extract_all_details():
    Title = check_product('span','id','productTitle')
    Description = check_product('ul','class','a-unordered-list a-vertical a-spacing-mini')
    Display_price = check_product('span','class','a-price-whole') + '.' + check_product('span','class','a-price-fraction')
    if browser.find_elements(By.XPATH,"//span[data-csa-c-type = 'element']")!=[]: 
        processing_time = check_product('span','data-csa-c-type','element')
    else:
        processing_time = 'Currenlty Unavailable'
    "Chanded Country to Canada so Shipping and Import Charges "
    if browser.find_elements(By.XPATH,"//div[@class='a-section a-spacing-none a-padding-none']") != []:
        # product_info_box = browser.find_element(By.XPATH,"//div[@class='a-section a-spacing-none a-padding-none']")
        Shipping_charge = browser.find_element(By.XPATH,"//div[@class='a-section a-spacing-none a-padding-none']//span[@class = 'a-size-base a-color-secondary']").text
    else:
        Shipping_charge = ''   
    Stock = check_product('div','id','availability')

    "Identifying selection"
    attributes = ['size','color']
    Size = ''
    Color = ''
    for attribute in attributes:
        if browser.find_elements(By.XPATH,f"//div[@id = 'variation_{attribute}_name']")!= []:
            # attribute_container = browser.find_element(By.XPATH,f"//div[@id = 'variation_{attribute}_name']")
            if attribute == 'size':
                Size = browser.find_element(By.XPATH,f"//div[@id = 'variation_{attribute}_name']//span[@class = 'selection']").text
            if attribute == 'color':
                Color = browser.find_element(By.XPATH,f"//div[@id = 'variation_{attribute}_name']//span[@class = 'selection']").text

    row = [Title,Description,Display_price,processing_time,Shipping_charge,Stock,Color,Size]
    image_list = extract_images()
    row += image_list
    
    for i in range(10 - len(image_list)):
        row.append('')
   
    print(row)
    return row

def scrape_elements(product_code):
    browser.get(f'https://amazon.com/dp/{str(product_code)}')
    print('\n')
    print('=====================================')
    print('Exctracting for product:',str(product_code))
    extract_all_details()
    

    
ASIN_LIST = ['B07BRK1PW4','B07GDLCQXV','B07XSCCZYG','B08MVFKGJM','B01DJLKZBA','B07XSCD2R4',
             'B07H515VCZ','B08BXBCNMQ','B0B9K44XTS','B07QZLHTTY','B01HIATG6I','B07QXD3J9G',
             'B081JDHNX1','B07DMBG7CX','B0B2X1BDFH','B07MXF4G8K']
for item in ASIN_LIST:
    # try:
    #     scrape_elements(item)
    # except Exception as Err:
    #     print(item,':Error')
    #     continue
    scrape_elements(item)


print(len(data),' rows collected')
df=pd.DataFrame(data,columns=['Title','Description','Display Price','Fastest Delivery Date','Shipping Charge','Stock','Color','Size',
                              'Image_1','Image_2','Image_3','Image_4','Image_5','Image_6','Image_6','Image_7','Image_8','Image_9','Image_10'])
df.to_csv('amazon-test.csv',index=False)
print('CSV created under sellvia-catalog-products.csv')
