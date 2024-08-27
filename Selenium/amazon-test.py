
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

options = Options()
options.headless = False
browser = webdriver.Firefox(options=options)
browser.fullscreen_window()
browser.execute_script("document.body.style.zoom='5%'")
data = []

def check_element(element_type,field,attribute_detail):
    WebDriverWait(browser,100000).until(EC.presence_of_element_located((By.XPATH,f"//{element_type}[@{field} = '{attribute_detail}']")))
    if browser.find_elements(By.XPATH,f"//{element_type}[@{field} = '{attribute_detail}']") != []:
        WebDriverWait(browser,100000).until(EC.presence_of_element_located((By.XPATH,f"//{element_type}[@{field} = '{attribute_detail}']")))
        output = browser.find_element(By.XPATH,f"//{element_type}[@{field} = '{attribute_detail}']").text 
        return output
    else:
        return ''
    
def check_product(element_type,field,attribute_detail):
    if browser.find_elements(By.XPATH,f"//{element_type}[{field} = '{attribute_detail}']")!=[]:
        return check_element(element_type,field,attribute_detail) 
    else:
        return ''



def extract_images():
    image_array  = []
    print('Extracting images')
    buttons =  browser.find_elements(By.XPATH,"//ul[contains(@class, 'a-unordered-list a-nostyle a-button-list a-vertical a-spacing-top-micro')]//input[@class='a-button-input']")
    first_image = browser.find_element(By.XPATH,"//img[@id = 'landingImage']").get_attribute('src')
    image_array.append(first_image)
    for i in range(len(buttons)):                         
        # print(i)
        button = browser.find_elements(By.XPATH,"//ul[contains(@class, 'a-unordered-list a-nostyle a-button-list a-vertical a-spacing-top-micro')]//input[@class='a-button-input']")[i]
        if button.is_displayed():     
            hover = ActionChains(browser).move_to_element(button)
            hover.perform()
            button.click()
            test_list = [image.get_attribute('src') for image in browser.find_elements(By.XPATH,"//img[@class = 'a-dynamic-image']")]
            image_array += test_list

    image_extraction = list(set(image_array))
    # print(image_extraction)
    print('lenght of image list:',len(image_extraction))
    return image_extraction


def extract_all_details():
    Title = check_element('span','id','productTitle')
    Description = check_element('ul','class','a-unordered-list a-vertical a-spacing-mini')
    Display_price = check_element('span','class','a-price-whole') + '.' + check_element('span','class','a-price-fraction')
    processing_time = check_product('span','data-csa-c-type','element')
    if browser.find_elements(By.XPATH,"//div[@class='a-section a-spacing-none a-padding-none']") != []:
        Shipping_charge = browser.find_element(By.XPATH,"//div[@class='a-section a-spacing-none a-padding-none']//span[@class = 'a-size-base a-color-secondary']").text
    else:
        Shipping_charge = ''   
    Stock = check_product('div','id','availability')

    "Identifying selection"
    attributes = ['size','color','style']
    Size = ''
    Color = ''
    Style = ''
    for attribute in attributes:
        if browser.find_elements(By.XPATH,f"//div[@id = 'variation_{attribute}_name']")!= []:
            WebDriverWait(browser,10000).until(EC.presence_of_element_located((By.XPATH,f"//div[@id = 'variation_{attribute}_name']")))
            if attribute == 'size':
                Size = browser.find_element(By.XPATH,f"//div[@id = 'variation_{attribute}_name']//span[@class = 'selection']").text
            if attribute == 'color':
                Color = browser.find_element(By.XPATH,f"//div[@id = 'variation_{attribute}_name']//span[@class = 'selection']").text
            if attribute == 'style':
                Style = browser.find_element(By.XPATH,f"//div[@id = 'variation_{attribute}_name']//span[@class = 'selection']").text

    row = [Title,Description,Display_price,processing_time,Shipping_charge,Stock,Color,Size,Style]
    image_list = extract_images()
    row += image_list
    
    for i in range(8 - len(image_list)):
        row.append('')
   
    # print(row)
    return row

def scrape_elements(product_code):
    browser.get(f'https://amazon.com/dp/{str(product_code)}')
    print('\n')
    print('=====================================')
    print('Exctracting for product:',str(product_code))
    data.append(extract_all_details())
    

    
ASIN_LIST = ['B07MXF4G8K','B08BXBCNMQ','B07BRK1PW4','B07GDLCQXV','B07XSCCZYG','B08MVFKGJM',
             'B01DJLKZBA','B07XSCD2R4','B0BMXYPFTK','B0CN6SLBGD']
for item in ASIN_LIST:
    try:
        scrape_elements(item)
    except Exception as Err:
        print(item,':Error')
        continue


print(len(data),' rows collected')
df=pd.DataFrame(data,columns=['Title','Description','Display Price','Fastest Delivery Date','Shipping Charge','Stock','Color','Size','Style',
                              'Image_1','Image_2','Image_3','Image_4','Image_5','Image_6','Image_6','Image_7'])
df.to_csv('amazon-test.csv',index=False)
print('CSV created under sellvia-catalog-products.csv')
