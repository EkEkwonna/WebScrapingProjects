from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

import string
import pandas as pd
options = Options()
options.headless = False
browser = webdriver.Firefox(options=options)
browser.fullscreen_window()
browser.execute_script("document.body.style.zoom='5%'")
data = []


"==========================================================="

"Function used for checking specific product attributes"

def check_product(element_type,field,attribute_detail):
    WebDriverWait(browser,20).until(EC.presence_of_element_located((By.XPATH,f"//{element_type}[@{field} = '{attribute_detail}']")))
    if browser.find_elements(By.XPATH,f"//{element_type}[@{field} = '{attribute_detail}']") != []:
        return browser.find_element(By.XPATH,f"//{element_type}[@{field} = '{attribute_detail}']").text
    else:
        return ''

def extract_description():
    if check_product('button','class','css-1l1iq20') != '':
        browser.find_element(By.XPATH,"//button[@class = 'css-1l1iq20']").click()
        return browser.find_element(By.XPATH,"//div[@data-automation= 'product-description-container']").text  
    else:
        return ''


"Desired Ouput"
"[Item , Description (including unit of measure), Current price, previous price, Size , Colour , discount]"
def extract_myer_details():
    title = check_product('h1','class','css-11xqsrc')
    current_display_price = check_product('p','class','css-1mxfaop')
    discount = check_product('p','class','discount-text')
    previous_price = check_product('p','data-automation','product-price-was')
    colour = check_product('span','data-automation','pdp-colour-display-value')
    description = extract_description()
    size = ''
    row = [title,description,current_display_price,previous_price,colour,size,discount]
    print(row)
    return row


def extract_david_jones_details():
    title = check_product('h1','itemprop','name')
    current_display_price = check_product('span','class','price-display')
    description = check_product('div','class','content long-description ql-editor')
    colour = check_product('span','class','colour-label')
    size = check_product('div','class','size-selection')
    previous_price = ''
    discount = ''
    row = [title,description,current_display_price,previous_price,colour,size,discount]




"==========================================================="
"Initiating Webscraping"

browser.get('https://www.myer.com.au')

"Random Sample list for www.myer.com.au"

myer_list = ["Organic Cotton Wardrobe Staple Long Sleeve Tee In Khaki",
             "Primula Coupe Dinner Set 12 Piece Gift Boxed in Pink",
             "Tea Party Runner 33x180cm in Multicolour",
             "Teas & C's Dahlia Daze Cotton Runner 150x33cm in Multi",
             "Lightsaber Squad Extendable Toy Lightsaber Assorted",
             "Star Wars Darth Vader Mech 75368",
             "SoundLink Revolve II Bluetooth Speaker 858365-0100",
             "Citiz & Milk Capsule Coffee Machine EN267BAE",
             "Bloom Quilt Cover Set in Stone"]

# for product in myer_list:
#     page_number = 1
#     browser.get(f'https://www.myer.com.au/search?query={product.replace(" ","+").replace("&","%26")}&pageNumber={page_number}')
#     item_found = 'No'

#     while item_found == 'No':
#         "Checking item in search results"
#         WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.XPATH,"//div[@data-automation = 'products-container']")))
#         container = browser.find_element(By.XPATH,"//div[@data-automation = 'products-container']")
        
#         if container.find_elements(By.XPATH,f'.//p[text()=\"{product}\"]') !=[]:
#             item_found = 'Yes'
#             located_item = container.find_element(By.XPATH,f'.//p[text()=\"{product}\"]').click()
#             data.append(extract_myer_details())
#         else:
#             page_number +=1

"Starting David Jones Extraction"

# browser.get('https://www.davidjones.com')

"Random sample list for from www.davidjones.com"
david_jones_list = ["T-RACE MOTOGP CHRONOGRAPH 2024 LIMITED EDITION WATCH",
                    "SEASTAR 1000 POWERMATIC 80 40MM WATCH",
                    "WOMEN'S SLOANE SANDAL",
                    "NEOCROC R LACOSTE BACKPACK SGNATURE",
                    "EXPLORAFUNK S MAILLE/CLF GLIT/SUE ME/CL ST/SP ASTR",
                    "MONO MUG",
                    "STARWARD SOLERA SINGLE MALT WHISKY 700ML",
                    "SQUARE SIGNATURE GRILLIT 26CM SATIN BLACK",
                    "MENS ACONCAGUA 3 VEST",
                    "ITALIAN MOLESKIN ITEM JACKET"]

for product in david_jones_list:
    browser.get(f'https://www.davidjones.com/search?q={product}'.replace(' ','+').replace("&","%26"))
    item_found = 'No'

    while item_found == 'No':
        "Checking item in search results"
        WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.XPATH,"//div[@class = 'products']")))
        container = browser.find_element(By.XPATH,"//div[@class = 'products']")
        print('here')
        if container.find_elements(By.XPATH,f'//a[text() = \"{product.title()}\"]') != []:
            item_found = 'Yes'
            located_item = browser.find_element(By.XPATH,f'//a[text() = \"{product.title()}\"]').click()
            data.append(extract_david_jones_details())
        elif container.find_elements(By.XPATH,f'//a[text() = \"{string.capwords(product)}\"]') != []:
            item_found = 'Yes'
            located_item = browser.find_element(By.XPATH,f'//a[text() = \"{string.capwords(product)}\"]').click()
            data.append(extract_david_jones_details())



# "Producing output CSV File"

# print(len(data),' rows collected')
# df = pd.DataFrame(data,columns=['Title','Description','Current Price','Previous Price','Colour','Discount'])
# df.to_csv('myer-david-jones.csv',index=False)
