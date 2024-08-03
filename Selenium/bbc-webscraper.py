
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

"Optional Headless bot"
options = Options()
options.headless = True

browser = webdriver.Firefox(options = options)
browser.get('https://www.bbc.co.uk')

"""
===================================================
DESIRED OUTPUT : CSV File containing the following 
News Article Title | Article URL Link | Created Date | Last Updated | Author 
===================================================
"""

articles = browser.find_elements(By.XPATH,"//*[contains(@class, 'ssrcss-its5xf-PromoLink exn3ah91') and contains(@href,'/news/article')]")
articleLInks = [[link.text,link.get_attribute('href')] for link in articles]

print(articleLInks)
print(len(articleLInks))

browser.close()







# article = browser.find_element(By.XPATH,"//a[@class = 'ssrcss-its5xf-PromoLink exn3ah91']")
# article_title = browser.find_element(By.XPATH,"//a[@class = 'ssrcss-its5xf-PromoLink exn3ah91']").text
# article_link = browser.find_element(By.XPATH,"//a[@class = 'ssrcss-its5xf-PromoLink exn3ah91']").get_attribute('href')

# tag = browser.find_element(By.XPATH,"//a[@class = 'ssrcss-1t4pp0s-MetadataLink e4wm5bw2']")
# tag_title = browser.find_element(By.XPATH,"//a[@class = 'ssrcss-1t4pp0s-MetadataLink e4wm5bw2']").text
# tag_link = browser.find_element(By.XPATH,"//a[@class = 'ssrcss-1t4pp0s-MetadataLink e4wm5bw2']").get_attribute('href')

# print(" | ",article_title, " | ",article_link, " | ", tag_title ," | ", tag_link)