
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

import time
import random
import pandas as pd


options = Options()
# options.add_argument('--headless=new')
browser = webdriver.Chrome( options=options)

# options = Options()
# options.headless = False
# browser = webdriver.Firefox(options=options)
# browser.fullscreen_window()
# browser.execute_script("document.body.style.zoom='5%'")
import json 

"""
Dictionary

Store .JSON
In format 

Questions {
    'Question 1: Question detail' : [
        'A. Answer 1'
        'B. Answer 2'
        'C. Answer 3'
        'D. Answer 4'
        'E. Answer 5'
    ]
}
"""


ALL_AMAZON_QUESTIONS = {}
TOTAL_NUMBER_OF_QUESTIONS = 981
# TOTAL_NUMBER_OF_QUESTIONS = 10
question_number = 1

url = f'https://www.google.com/search?q=Amazon+AWS+Certified+Solutions+Architect+-+Associate+SAA-C03+Topic+1+question+{str(question_number)}'

def random_delay():
    return random.randint(2,5)

def extract_question_and_answers():
    # WebDriverWait(browser,20).until(EC.presence_of_element_located((By.XPATH,"//a[contains(text(),'Show Suggested Answer')]")))
    # browser.find_element(By.XPATH,"//a[contains(text(),'Show Suggested Answer')]").click()
    question = browser.find_element(By.XPATH,"//p[@class = 'card-text']").text
    browser.find_element(By.XPATH,"//a[@class ='btn btn-primary reveal-solution']").click()
    correct_answers = [(item.text,True) for item in browser.find_elements(By.XPATH,"//ul//li[@class = 'multi-choice-item correct-hidden correct-choice']")]
    # print('correct answer: \n',correct_answers)
    incorrect_answers = [(item.text,False) for item in browser.find_elements(By.XPATH,"//ul//li[@class = 'multi-choice-item']")]
    all_answers = correct_answers + incorrect_answers
    # print(all_answers)
    ALL_AMAZON_QUESTIONS[f'QUESTION : {str(question_number)}'] = {'question': question ,
                                                                  'answers' : sorted([answer[0] for answer in all_answers]),
                                                                  'correct' : correct_answers}
    print(f'------QUESTION:{question_number} ------')
    print(question)
    print('---------ANSWERS-------')
    for answer_ in sorted(all_answers):
        print(answer_[0], ' : ', answer_[1],'\n')


for question in range(1,TOTAL_NUMBER_OF_QUESTIONS +1):
    # time.sleep(random_delay())
    browser.get(f'https://www.google.com/search?q=Amazon+AWS+Certified+Solutions+Architect+-+Associate+SAA-C03+Topic+1+question+{str(question_number)}')
    if browser.find_elements(By.XPATH,"//div[@class = 'QS5gu sy4vM']") != []:
        browser.find_element(By.XPATH,"//div[@class = 'QS5gu sy4vM']").click()
    browser.find_element(By.XPATH,"//div[@class = 'dURPMd']//div").click()
    extract_question_and_answers()
    question_number +=1

with open('CAA-CO3-Qs.json','w') as w:
    json.dumps(ALL_AMAZON_QUESTIONS,w)
