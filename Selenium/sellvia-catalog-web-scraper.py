
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

def extract_images():
    image_array=set()
    first_image = browser.find_element(By.XPATH,"//img[@class='makezoom']").get_attribute('src')
    if first_image[-10:] == '-full.jpeg':
        first_image = first_image[:-10]
    image_array.add(first_image)
    current_image = 0
    for i in range(15):
        browser.find_element(By.XPATH,"//div[@class='slider-next']").click()
        current_image = browser.find_element(By.XPATH,"//img[@class='makezoom']").get_attribute('src')
        if current_image[-10:] == '-full.jpeg':
            current_image = current_image[:-10]
        if current_image != first_image:
            image_array.add(current_image)
        else:
            break
    return list(image_array)

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
    WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.XPATH,"//h1[@class='h4']")))
    WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.XPATH,"//span[@class = 'number']")))
    product_title = browser.find_element(By.XPATH,"//h1[@class='h4']").text
    display_price = browser.find_element(By.XPATH,"//span[@class = 'number']").text
    retail_price = browser.find_element(By.XPATH,"//div[@class = 'product-single-retail']").text
    description = browser.find_element(By.XPATH,"//div[@class='wrap-content']").text
    image_list = extract_images()
    processing_time = browser.find_element(By.XPATH,"//div[@class='single-shipping_title']").text.split(': ')[1]
    shipping_and_handling = float(browser.find_element(By.XPATH,"//span[@class = 'js-sku-shipping-price']").text.split('$')[1])
        
    "Checking Stock Levels"
    WebDriverWait(browser, 10)
    if browser.find_elements(By.XPATH,"//div[@class='stock']")!=[]:
        stock = browser.find_element(By.XPATH,"//div[@class='stock']").text
    elif browser.find_elements(By.XPATH,"//div[@class='stock outofstock']") != []:
        print(browser.find_element(By.XPATH,"//div[@class='stock outofstock']").text )
        stock = browser.find_element(By.XPATH,"//div[@class='stock outofstock']").text
    else:
        stock = 'Undetermined' 

    "Identifying Options"
    [Type,Size,Color] = ['Type','Size','Color']
    feature_options = [Type,Size,Color]
    for i in range(len(feature_options)):
        if len(browser.find_elements(By.XPATH,f"//div[@class='name' and (contains(text(),'{feature_options[i]}'))]")) == 1:
            element_containing_option=browser.find_element(By.XPATH,f"//div[@class='name' and contains(text(),'{feature_options[i]}')]")
            if element_containing_option.find_elements(By.XPATH,".//span[@style = 'margin: 0px 0px 0px 5px;']") !=[]:
                feature_options[i] = element_containing_option.find_element(By.XPATH,".//span[@style = 'margin: 0px 0px 0px 5px;']").text
            else:
                feature_options[i] = ''
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
    print('\n')
    print('=====================================')
    print('Exctracting for product:',str(product_code))
    
    "Testing for 2 ranges of available options"
    "One range is images and second is text"
    "Word options"
    word_options = [item.text for item in browser.find_elements(By.XPATH,"//span[contains(@class,'js-sku-set meta-item meta-item-text is-not-empty')]")]
    "Image options"
    image_options = [item.get_attribute('title') for item in browser.find_elements(By.XPATH,"//img[@class = 'img-responsive']")]
    print('word options:',word_options,'image options:',image_options)
    if len(browser.find_elements(By.XPATH,"//div[@class='value']")) ==2:
        if word_options!=[] and image_options !=[] and word_options[0]!='':
            first_range_of_options = image_options
            second_range_of_options = word_options
            for first_section_option in first_range_of_options:
                for second_section_option in second_range_of_options:
                    WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH,f"//span[contains(@data-title,'{first_section_option}')]")))
                    button1 = browser.find_element(By.XPATH,f"//img[@title='{first_section_option}']").click()
                    print(first_section_option,' selected')
                    WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH,f"//span[contains(@data-title,'{second_section_option}')]")))
                    button2 = browser.find_element(By.XPATH,f"//span[@data-title='{second_section_option}']").click()
                    print(second_section_option,' selected')
                    data_entry = extract_all_details()
                    data.append(data_entry)    

    "Both ranges of available options are text"
    if len(browser.find_elements(By.XPATH,"//div[@class='value']")) ==2:
        if browser.find_element(By.XPATH,"//div[@class='value']")!=[]:
            first_section=browser.find_element(By.XPATH,"//div[@class='value']")
            first_range_of_options = [item.text for item in first_section.find_elements(By.XPATH,".//span[contains(@class,'js-sku-set meta-item meta-item-text is-not-empty')]")]
            second_section=browser.find_elements(By.XPATH,"//div[@class='value']")[1]
            second_range_of_options = [item.text for item in second_section.find_elements(By.XPATH,".//span[contains(@class,'js-sku-set meta-item meta-item-text is-not-empty')]")]
            for first_section_option in first_range_of_options:
                for second_section_option in second_range_of_options:
                    WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH,f"//span[contains(@data-title,'{first_section_option}')]")))
                    button1 = browser.find_element(By.XPATH,f"//span[@data-title='{first_section_option}']").click()
                    print(first_section_option,' selected')
                    WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH,f"//span[contains(@data-title,'{second_section_option}')]")))
                    button2 = browser.find_element(By.XPATH,f"//span[@data-title='{second_section_option}']").click()
                    print(second_section_option,' selected')
                    data_entry = extract_all_details()
                    data.append(data_entry)    
    else:
        "Testing for word options"
        available_options = [item.text for item in browser.find_elements(By.XPATH,"//span[contains(@class,'js-sku-set meta-item meta-item-text is-not-empty')]")]
        
        "Testing for image options"
        available_options2 = [item.get_attribute('title') for item in browser.find_elements(By.XPATH,"//img[@class = 'img-responsive']")]
        if len(available_options) >=2:
            for option in available_options:
                WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH,f"//span[contains(@data-title,'{option}')]")))
                button = browser.find_element(By.XPATH,f"//span[@data-title='{option}']").click()
                print(option,' selected')
                data_entry = extract_all_details()
                data.append(data_entry)
            return
        if len(available_options2) >=2:
            for option in available_options2:
                WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.XPATH,f"//img[@class = 'img-responsive' and contains(@title,'{option}')]")))
                button = browser.find_element(By.XPATH,f"//img[@class = 'img-responsive' and contains(@title,'{option}')]").click()
                print(option,' selected')
                data_entry = extract_all_details()
                data.append(data_entry)
        else:
            data_entry = extract_all_details()
            data.append(data_entry)
    

for item in range(1659920,1659900,-1):
    try:
        scrape_elements(item)
    except Exception as Err:
        print(item,':Error')
        continue

print(len(data),' rows collected')
df=pd.DataFrame(data,columns=['Title','Description','Display Price USD($)','Retail Price USD($)','Processing Time','Shipping and Handling USD ($)','Type','Size','Color',
                              'Image_1','Image_2','Image_3','Image_4','Image_5','Image_6','Image_7','Image_8','Image_9','Image_10',
                              'Image_11','Image_12','Image_13','Image_14','Image_15',
                              'Processing Time','In Stock',
                              #hidden_fields
                              'post_id','currency','_price','_price_nc','_save','_save_nc','stock','savePercent','_salePrice','_salePrice_nc',
                                'price','salePrice','save','single_shipping_price','currency_shipping','variation_default','shipping','sku-meta','sku-meta-set[]'])

df.to_csv('sellvia-catalog-products.csv',index=False)
print('CSV created under sellvia-catalog-products.csv')
