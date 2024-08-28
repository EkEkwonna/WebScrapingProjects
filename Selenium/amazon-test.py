
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

options = Options()
options.headless = True
browser = webdriver.Firefox(options=options)
browser.fullscreen_window()
browser.execute_script("document.body.style.zoom='5%'")
data = []

def check_element(element_type,field,attribute_detail):
    # WebDriverWait(browser,100000).until(EC.presence_of_element_located((By.XPATH,f"//{element_type}[@{field} = '{attribute_detail}']")))
    if browser.find_elements(By.XPATH,f"//{element_type}[@{field} = '{attribute_detail}']") != []:
        # WebDriverWait(browser,100000).until(EC.presence_of_element_located((By.XPATH,f"//{element_type}[@{field} = '{attribute_detail}']")))
        output = browser.find_element(By.XPATH,f"//{element_type}[@{field} = '{attribute_detail}']").text 
        return output
    else:
        return ''
    
def random_delay():
    return random.randint(2,10)


def check_product(element_type,field,attribute_detail):
    if browser.find_elements(By.XPATH,f"//{element_type}[{field} = '{attribute_detail}']")!=[]:
        return check_element(element_type,field,attribute_detail) 
    else:
        return ''



def extract_images():
    image_array  = []
    print('Extracting images')
    if browser.find_elements(By.XPATH,"//ul[contains(@class, 'a-unordered-list a-nostyle a-button-list a-vertical a-spacing-top-micro')]//img[@id='landingImage']") != [] and browser.find_element(By.XPATH,"//ul[contains(@class, 'a-unordered-list a-nostyle a-button-list a-vertical a-spacing-top-micro')]//img[@id='landingImage']").is_displayed():
        landingImage = browser.find_element(By.XPATH,"//ul[contains(@class, 'a-unordered-list a-nostyle a-button-list a-vertical a-spacing-top-micro')]//img[@id='landingImage']").get_attribute('src')
        image_array.append(landingImage)
    buttons =  browser.find_elements(By.XPATH,"//ul[contains(@class, 'a-unordered-list a-nostyle a-button-list a-vertical a-spacing-top-micro')]//input[@class='a-button-input']")
    for i in range(len(buttons)):                         
        print(i)
        button = browser.find_elements(By.XPATH,"//ul[contains(@class, 'a-unordered-list a-nostyle a-button-list a-vertical a-spacing-top-micro')]//input[@class='a-button-input']")[i]
        if button.is_displayed():     
            hover = ActionChains(browser).move_to_element(button)
            hover.perform()
            button.click()
            test_list = [image.get_attribute('src') for image in browser.find_elements(By.XPATH,"//img[@class = 'a-dynamic-image']")]
            image_array += test_list
    
    browser.refresh()
    image_extraction = list(set(image_array))
    print(image_extraction)
    print('lenght of image list:',len(image_extraction))
    return image_extraction


def extract_all_details(attribute_dimensions):
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
    attribute_dimensions
    Size = ''
    Color = ''
    Style = ''
    # browser.refresh()
    for attribute in attribute_dimensions:
        if browser.find_elements(By.XPATH,f"//div[@id = 'variation_{attribute}_name']")!= []:
            # ActionChains(browser).move_to_element(browser.find_element(By.XPATH,f"//div[@id = 'variation_{attribute}_name']")).perform()
            # WebDriverWait(browser,100).until(EC.element_to_be_clickable((By.XPATH,f"//div[@id = 'variation_{attribute}_name']//span[@class = 'selection']")))
            if attribute == 'size':
                print('Extracting size')
                browser.refresh()
                Size = browser.find_element(By.XPATH,f"//div[@id = 'variation_{attribute}_name']//span[@class = 'selection']").text
            if attribute == 'color':
                print('Extracting Color')
                Color = browser.find_element(By.XPATH,f"//div[@id = 'variation_{attribute}_name']//span[@class = 'selection']").text
            if attribute == 'style':
                print('Extracting style')
                Style = browser.find_element(By.XPATH,f"//div[@id = 'variation_{attribute}_name']//span[@class = 'selection']").text

    row = [item,Title,Description,Display_price,processing_time,Shipping_charge,Stock,Color,Size,Style]
    "If we have 2 adjecent rows with the same product title and same color no pictures selected"
    if len(data)!= 0 :
        print("------------------------------------------")
        print(data[len(data)-1][0],data[len(data) -1][0],data[len(data) -1][7])
        print(item,Color,Title)
        print('-------------------------------')

    if len(data) !=0 and data[len(data)-1][7]== Color and item == data[len(data)-1][0]:
        image_list = ['']
    else:
        browser.refresh()
        image_list = extract_images()
        
    row += image_list
    
    for i in range(8 - len(image_list)):
        row.append('')

    print(row)
    return row

def scrape_elements(attribute_dimensions):
    data.append(extract_all_details(attribute_dimensions))
    

    
ASIN_LIST = ['B07MXF4G8K','B08BXBCNMQ','B07BRK1PW4','B07GDLCQXV','B07XSCCZYG','B08MVFKGJM',
             'B01DJLKZBA','B07XSCD2R4','B0BMXYPFTK','B0CN6SLBGD']
for item in ASIN_LIST:
    # try:
    #     scrape_elements(item)
    # except Exception as Err:
    #     print(item,':Error')
    #     continue
    browser.get(f'https://amazon.com/dp/{item}')
    print('\n')
    print('=====================================')
    print('Exctracting for product:',str(item))
    # WebDriverWait(browser,100).until(EC.presence_of_element_located((By.XPATH,"//div[@id = 'centerCol']")))
    available_options_sections = browser.find_elements(By.XPATH,"//div[@id = 'centerCol']//ul[contains(@class,'a-unordered-list')]")
    print(len(available_options_sections)-1,'Number of sections detected')
    if len(available_options_sections) == 2:
        section = browser.find_element(By.XPATH,"//div[@id = 'centerCol']//ul")
        section_options = [(item.get_attribute('id'),item.get_attribute('class'),item.get_attribute('title').split('Click to select ')[1]) for item in section.find_elements(By.XPATH, ".//li")]
        print(section_options)
        for section_option in section_options:
            if section_option[1] != 'swatchUnavailable':
                # WebDriverWait(browser,100).until(EC.presence_of_element_located((By.XPATH,f"//li[@id ='{section_option[0]}']")))
                browser.find_element(By.XPATH,f"//li[@id ='{section_option[0]}']").click()
                attribute_dimensions = [section_option.split('_')[0]]    
                scrape_elements(attribute_dimensions)

    if len(available_options_sections) == 3:
        first_section = browser.find_element(By.XPATH,"//div[@id = 'centerCol']//ul[contains(@class,'a-unordered-list')]")
        first_section_options = [(list_item.get_attribute('id'),list_item.get_attribute('class')) for list_item in first_section.find_elements(By.XPATH,".//li")]
        print("First Section",first_section_options)
        for first_section_item in first_section_options:
            # WebDriverWait(browser,100).until(EC.presence_of_element_located((By.XPATH,f"//li[@id ='{first_section_item[0]}']")))
            browser.find_element(By.XPATH,f"//li[@id ='{first_section_item[0]}']").click()
            second_section = browser.find_elements(By.XPATH,"//div[@id = 'centerCol']//ul[contains(@class,'a-unordered-list')]")[1]
            second_section_options = [(list_item.get_attribute('id'),list_item.get_attribute('class')) for list_item in second_section.find_elements(By.XPATH,".//li")]
            print('Second Section',second_section_options)
            for second_section_option in second_section_options:
                if second_section_option[1] != 'swatchUnavailable':
                    # WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.XPATH,f"//li[@id = '{second_section_option[0]}']"))) 
                    element = browser.find_element(By.XPATH,f"//li[@id = '{second_section_option[0]}']")
                    ActionChains(browser).move_to_element(element).click().perform()
                    # browser.find_element(By.XPATH,f"//li[@id = '{second_section_option[0]}']").click()
                    attribute_dimensions = [first_section_item.split('_')[0],second_section_option.split('_')[0]]
                    scrape_elements(attribute_dimensions)

    if len(available_options_sections) ==4:
        first_section = browser.find_element(By.XPATH,"//div[@id = 'centerCol']//ul[contains(@class,'a-unordered-list')]")
        first_section_options = [(list_item.get_attribute('id'),list_item.get_attribute('class')) for list_item in first_section.find_elements(By.XPATH,".//li")]
        print("First Section",first_section_options)
        for first_section_item in first_section_options:
            # WebDriverWait(browser,100).until(EC.element_to_be_clickable((By.XPATH,f"//li[@id ='{first_section_item[0]}']")))
            browser.find_element(By.XPATH,f"//li[@id ='{first_section_item[0]}']").click()
            second_section = browser.find_elements(By.XPATH,"//div[@id = 'centerCol']//ul[contains(@class,'a-unordered-list')]")[1]
            second_section_options = [(list_item.get_attribute('id'),list_item.get_attribute('class')) for list_item in second_section.find_elements(By.XPATH,".//li")]
            print('Second Section',second_section_options)
            for second_section_option in second_section_options:
                if second_section_option[1] != 'swatchUnavailable':
                    # WebDriverWait(browser,100).until(EC.element_to_be_clickable((By.XPATH,f"//li[@id = '{second_section_option[0]}']")))
                    browser.find_element(By.XPATH,f"//li[@id = '{second_section_option[0]}']").click()
                    third_section = browser.find_elements(By.XPATH,"//div[@id = 'centerCol']//ul[contains(@class,'a-unordered-list')]")[2]
                    third_section_options = [(list_item.get_attribute('id'),list_item.get_attribute('class')) for list_item in third_section.find_elements(By.XPATH,".//li")]
                    print('Third Section',second_section_options)
                    for third_section_option in third_section_options:
                        if third_section_option[1]  != 'swatchUnavailable':
                            # WebDriverWait(browser,100).until(EC.presence_of_element_located((By.XPATH,f"//li[@id = '{third_section_option[0]}']")))
                            browser.find_element(By.XPATH,f"//li[@id = '{third_section_option[0]}']").click()
                            attribute_dimensions = [first_section_item.split('_')[0],second_section_option.split('_')[0],third_section_option.split('_')[0]]
                            scrape_elements(attribute_dimensions)
    else:
        scrape_elements()
        
            




print(len(data),' rows collected')
df=pd.DataFrame(data,columns=['ASIN','Title','Description','Display Price','Fastest Delivery Date','Shipping Charge','Stock','Color','Size','Style',
                              'Image_1','Image_2','Image_3','Image_4','Image_5','Image_6','Image_6','Image_7'])
df.to_csv('amazon-test.csv',index=False)
print('CSV created under sellvia-catalog-products.csv')
