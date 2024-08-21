from bs4 import BeautifulSoup
import requests

url = 'https://www.bbc.co.uk/news'
response = requests.get(url)
soup = BeautifulSoup(response.text,'html.parser')

class_text = 
print(soup.find_all("a",class_=class_text))
