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
browser.execute_script("document.body.style.zoom='5%'")
data = []

browser.get('https://buildsteel.org/products-and-providers/')
providers = [(tag.get_attribute('data-order-default'),tag.get_attribute('href')) for tag in browser.find_elements(By.XPATH,"//a[contains(@class,'wpupg-item wpupg-item-post')]")]

def extract_field(attribute):
    Info_box = browser.find_element(By.XPATH,"//aside[@class='sidebar sidebar--supplier']")
    if Info_box.find_elements(By.XPATH,f".//a[contains(@href,'{attribute}')]") != []:
        return Info_box.find_element(By.XPATH,f".//a[contains(@href,'{attribute}')]").text
    else:
        return 'Not Provided'
    return

def extract_contact():
    "Verifying Contact exist"
    Info_box = browser.find_element(By.XPATH,"//aside[@class='sidebar sidebar--supplier']")
    if Info_box.find_elements(By.XPATH,".//p") !=[]:
        return Info_box.find_elements(By.XPATH,".//p")[0].text.replace('\n',' ')
    else:
        return 'Not Provided'


for provider in providers:
    browser.get(provider[1])
    title = provider[0]

    contact = extract_contact()
    telephone=extract_field('tel:').replace('.','')
    email = extract_field('mailto:')
    website = extract_field('http')
    row = [title,contact,telephone,email,website]
    print(row)
    data.append(row)

print(len(data),' rows collected')
df = pd.DataFrame(data,columns=['Title','Address','Telephone','Email','Website'])
df.to_csv('buildSteelProviders.csv',index=False)
