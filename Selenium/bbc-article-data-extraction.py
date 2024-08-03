
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd

"Optional Headless bot"
options = Options()
options.headless = True

browser = webdriver.Firefox(options = options)
browser.get('https://www.bbc.co.uk')



"Author information presented in different styles for each article"
def author_extraction():
    authors = ''
    try:
        if browser.find_elements(By.XPATH,"//div[@class='ssrcss-68pt20-Text-TextContributorName e8mq1e96']") != []:
            author_names = [author_element.text for author_element in browser.find_elements(By.XPATH,"//div[@class='ssrcss-68pt20-Text-TextContributorName e8mq1e96']")]
            authors += ' , '.join(author_names)
            
        elif browser.find_elements(By.XPATH,"//div[@class=ssrcss-lo1ylm-StyledLink e8mq1e92']") != []:
            author_names = [author_element.text for author_element in browser.find_elements(By.XPATH,"//div[@class=ssrcss-lo1ylm-StyledLink e8mq1e92']")]
            authors += ' , '.join(author_names)
    except Exception:
        authors+= 'No Author info'

    return authors


"Waiting for all the HTML classes to load"
elem = WebDriverWait(browser,20).until(EC.presence_of_element_located((By.XPATH,"//*[contains(@class, 'ssrcss-its5xf-PromoLink exn3ah91') and contains(@href,'/news/article')]")))


articles = browser.find_elements(By.XPATH,"//*[contains(@class, 'ssrcss-its5xf-PromoLink exn3ah91') and contains(@href,'/news/article')]")
articleLinks = [[link.text,link.get_attribute('href')] for link in articles]
print(len(articleLinks),' articles located')

for article in articleLinks:
    browser.get(str(article[1]))
    createdTimestamp = browser.find_element(By.XPATH,"//time[@data-testid = 'timestamp']").text
    author = author_extraction()
    article+= [createdTimestamp,author]
    print(article)


for article in articleLinks: 
    print(article)

browser.quit()


"""
===================================================
DESIRED OUTPUT : CSV File containing the following 
News Article Title | Article URL Link | Created Date | Author(s) 
===================================================
"""



df=pd.DataFrame(articleLinks,columns=['Title','URL','Created Date','Author(s)'])
print(df.head())

# df.to_csv('BBC-NEWS-ARTICLE-DATA.csv')