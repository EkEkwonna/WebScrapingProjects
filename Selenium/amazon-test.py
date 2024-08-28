
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
        WebDriverWait(browser,100000).until(EC.presence_of_element_located((By.XPATH,f"//{element_type}[@{field} = '{attribute_detail}']")))
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
    """
    identify button section 
    create alist of all the list items with imageThumbnail in the class
    for list item if displayed click use data-csa-c-posy
    """
    time.sleep(random_delay())


    thumbnail_ids = [thumbnail.get_attribute('data-csa-c-posy') for thumbnail in browser.find_elements(By.XPATH,"//ul[contains(@class, 'a-unordered-list a-nostyle a-button-list a-vertical')]//li[@data-csa-c-posy and contains(@class,'imageThumbnail')]")]
    for thumbnail_ID in thumbnail_ids:
        current_thumbnail = browser.find_element(By.XPATH,f"//li[@data-csa-c-posy = '{thumbnail_ID}']")
        if current_thumbnail.is_displayed():
            current_thumbnail.click()
            if browser.find_elements(By.XPATH,"//i[@class='a-icon a-icon-close']") !=[] and browser.find_element(By.XPATH,"//i[@class='a-icon a-icon-close']").is_displayed() :
                time.sleep(random_delay())
                browser.find_element(By.XPATH,"//i[@class='a-icon a-icon-close']").click()

            test_list = [image.get_attribute('src') for image in browser.find_elements(By.XPATH,"//img[contains(@class, 'a-dynamic-image')]") if (image.is_displayed() and image.get_attribute('src')[:26] == 'https://m.media-amazon.com')]
            image_array += test_list
    
    image_extraction = list(set(image_array))
    # print(image_extraction)
    # print('lenght of image list:',len(image_extraction))
    return image_extraction

def extract_all_details(attribute_dimensions):
    ASIN_VALUE = browser.current_url.split('?')[0].split('www.amazon.com/dp/')[1]
    Title = check_element('span','id','productTitle')
    Description = check_element('ul','class','a-unordered-list a-vertical a-spacing-mini')
    processing_time = check_product('span','data-csa-c-type','element')
    image_test = extract_images()
    Display_price = ''
    if browser.find_elements(By.XPATH,"//div[@class='a-section a-spacing-none a-padding-none']") != []:
        if browser.find_elements(By.XPATH,"//div[@class='a-section a-spacing-none a-padding-none']//span[@class = 'a-price-whole']") != []:
            Display_price = browser.find_element(By.XPATH,"//div[@class='a-section a-spacing-none a-padding-none']//span[@class = 'a-price-whole']").text + '.' + browser.find_element(By.XPATH,"//div[@class='a-section a-spacing-none a-padding-none']//span[@class = 'a-price-fraction']").text

        if browser.find_elements(By.XPATH,"//div[@class='a-section a-spacing-none a-padding-none']//span[@class = 'a-size-base a-color-secondary']") != []:
            Shipping_charge = browser.find_element(By.XPATH,"//div[@class='a-section a-spacing-none a-padding-none']//span[@class = 'a-size-base a-color-secondary']").text
        else:
            Shipping_charge = 'N/A' + browser.find_element(By.XPATH,"//div[@class='a-section a-spacing-none a-padding-none']//span[@class = 'a-color-error']").text
    else:
        Shipping_charge = ''   
    Stock = check_product('div','id','availability')

    "Identifying selection"
    attribute_dimensions
    Size = ''
    Color = ''
    Style = ''
    for attribute in attribute_dimensions:
        if browser.find_elements(By.XPATH,f"//div[@id = 'variation_{attribute}_name']")!= []:
            if attribute == 'size':
                WebDriverWait(browser,20).until(EC.presence_of_element_located((By.XPATH,f"//div[@id = 'variation_{attribute}_name']//span[@class = 'selection']")))
                Size = browser.find_element(By.XPATH,f"//div[@id = 'variation_{attribute}_name']//span[@class = 'selection']").text
            if attribute == 'color':
                WebDriverWait(browser,20).until(EC.presence_of_element_located((By.XPATH,f"//div[@id = 'variation_{attribute}_name']//span[@class = 'selection']")))
                Color = browser.find_element(By.XPATH,f"//div[@id = 'variation_{attribute}_name']//span[@class = 'selection']").text
            if attribute == 'style':
                WebDriverWait(browser,20).until(EC.presence_of_element_located((By.XPATH,f"//div[@id = 'variation_{attribute}_name']//span[@class = 'selection']")))
                Style = browser.find_element(By.XPATH,f"//div[@id = 'variation_{attribute}_name']//span[@class = 'selection']").text

    image_list = image_test
        
    if len(image_list) < 9:
        for i in range(9 - len(image_list)):
            image_list.append('')

    row = [ASIN_VALUE,Title,Description,Display_price,processing_time,Shipping_charge,Stock,Color,Size,Style]
    "If we have 2 adjecent rows with the same product title and same color no pictures selected"


    print("-------------ADDING ROW-------------------")
    print(ASIN_VALUE,':',Title,',',Color,',',Size,',',Style,',',Display_price)
    print('------------------------------------------')

    
    row += image_list

    return row

def scrape_elements(attribute_dimensions):
    try:
        data.append(extract_all_details(attribute_dimensions))
    except Exception as Err:
        print(Err)

    

    
ASIN_LIST = [
    # 'B07MXF4G8K','B08BXBCNMQ','B07BRK1PW4','B07GDLCQXV','B07XSCCZYG','B01DJLKZBA','B07XSCD2R4',
    'B08MVFKGJM','B0032JUOU2','B0D7M3ZJ1Z','B0BMXYPFTK','B0CN6SLBGD'
             ]
for item in ASIN_LIST:
    browser.get(f'https://amazon.com/dp/{item}')
    print('\n')
    print('=====================================')
    print('Observing product with ASIN:',str(item))
    available_options_sections = browser.find_elements(By.XPATH,"//div[@id = 'centerCol']//ul[contains(@class,'a-unordered-list')]")

    if len(available_options_sections) == 2:
        section = browser.find_element(By.XPATH,"//div[@id = 'centerCol']//ul")
        section_options = [(item.get_attribute('id'),item.get_attribute('class'),item.get_attribute('title').split('Click to select ')[1]) for item in section.find_elements(By.XPATH, ".//li")]
        # print(section_options)
        for section_option in section_options:
            if section_option[1] != 'swatchUnavailable':
                browser.find_element(By.XPATH,f"//li[@id ='{section_option[0]}']").click()
                attribute_dimensions = [section_option[0].split('_')[0]]
                print('Attributes detected:',section_option[0].split('_')[0])    
                scrape_elements(attribute_dimensions)
                browser.refresh()

    if len(available_options_sections) == 3:
        first_section = browser.find_element(By.XPATH,"//div[@id = 'centerCol']//ul[contains(@class,'a-unordered-list')]")
        first_section_options = [(list_item.get_attribute('id'),list_item.get_attribute('class'),list_item.get_attribute('title').split('Click to select ')[1]) for list_item in first_section.find_elements(By.XPATH,".//li")]
        # print("First Section",first_section_options)
        for first_section_item in first_section_options:
            WebDriverWait(browser,200).until(EC.presence_of_element_located((By.XPATH,f"//li[@id ='{first_section_item[0]}']")))
            browser.find_element(By.XPATH,f"//li[@id ='{first_section_item[0]}']").click()
            second_section = browser.find_elements(By.XPATH,"//div[@id = 'centerCol']//ul[contains(@class,'a-unordered-list')]")[1]
            second_section_options = [(list_item.get_attribute('id'),list_item.get_attribute('class'),list_item.get_attribute('title').split('Click to select ')[1]) for list_item in second_section.find_elements(By.XPATH,".//li")]
            # print('Second Section',second_section_options)
            for second_section_option in second_section_options:
                if second_section_option[1] != 'swatchUnavailable':
                    WebDriverWait(browser,200).until(EC.element_to_be_clickable((By.XPATH,f"//li[@id = '{second_section_option[0]}']")))
                    browser.find_element(By.XPATH,f"//li[@id = '{second_section_option[0]}']").click()
                    attribute_dimensions = [first_section_item[0].split('_')[0],second_section_option[0].split('_')[0]]
                    print('Attributes detected',first_section_item[0].split('_')[0],',',second_section_option[0].split('_')[0])
                    scrape_elements(attribute_dimensions)
                    browser.refresh()

    if len(available_options_sections) ==4:
        first_section = browser.find_element(By.XPATH,"//div[@id = 'centerCol']//ul[contains(@class,'a-unordered-list')]")
        first_section_options = [(list_item.get_attribute('id'),list_item.get_attribute('class'),list_item.get_attribute('title').split('Click to select ')[1]) for list_item in first_section.find_elements(By.XPATH,".//li")]
        # print("First Section",first_section_options)
        for first_section_item in first_section_options:

            browser.find_element(By.XPATH,f"//li[@id ='{first_section_item[0]}']").click()
            second_section = browser.find_elements(By.XPATH,"//div[@id = 'centerCol']//ul[contains(@class,'a-unordered-list')]")[1]
            second_section_options = [(list_item.get_attribute('id'),list_item.get_attribute('class'),list_item.get_attribute('title').split('Click to select ')[1]) for list_item in second_section.find_elements(By.XPATH,".//li")]
            # print('Second Section',second_section_options)
            for second_section_option in second_section_options:
                if second_section_option[1] != 'swatchUnavailable':

                    browser.find_element(By.XPATH,f"//li[@id = '{second_section_option[0]}']").click()
                    third_section = browser.find_elements(By.XPATH,"//div[@id = 'centerCol']//ul[contains(@class,'a-unordered-list')]")[2]
                    third_section_options = [(list_item.get_attribute('id'),list_item.get_attribute('class'),list_item.get_attribute('title').split('Click to select ')[1]) for list_item in third_section.find_elements(By.XPATH,".//li")]
                    # print('Third Section',third_section_options)
                    for third_section_option in third_section_options:
                        if third_section_option[1]  != 'swatchUnavailable':

                            browser.find_element(By.XPATH,f"//li[@id = '{third_section_option[0]}']").click()
                            attribute_dimensions = [first_section_item[0].split('_')[0],second_section_option[0].split('_')[0],third_section_option[0].split('_')[0]]
                            print('Attributes detected:',first_section_item[0].split('_')[0],',',second_section_option[0].split('_')[0],',',third_section_option[0].split('_')[0])
                            scrape_elements(attribute_dimensions)
                            browser.refresh()
    else:
        scrape_elements([])
        
            




print(len(data),' rows collected')
for data_row in data: 
    print(len(data_row))


df=pd.DataFrame(data,columns=['ASIN','Title','Description','Display Price','Fastest Delivery Date','Shipping Charge','Stock','Color','Size','Style',
                              'Image_1','Image_2','Image_3','Image_4','Image_5','Image_6','Image_7','Image_8','Image_9'])
df.to_csv('amazon-test.csv',index=False)
print('CSV created under sellvia-catalog-products.csv')
