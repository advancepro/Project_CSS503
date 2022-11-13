import urllib.request
import webbrowser

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

from selenium.webdriver.common.by import By

url = 'https://arbuz.kz/'
webbrowser.open_new_tab(url)


webUrl = urllib.request.urlopen('https://arbuz.kz/')

print("result code: " + str(webUrl.getcode()))



import urllib.request, urllib.parse, urllib.error

user_url = 'https://arbuz.kz/#/'
handle = urllib.request.urlopen(user_url)
result = handle.read()
print(len(result))

handle = urllib.request.urlopen(user_url)
result = handle.read(3000)

import requests
from bs4 import BeautifulSoup

url = 'https://arbuz.kz/#/'
fr = []
wanted = ['Yoghurt','Parsley','Radish']
a = requests.get(url).text
soup = BeautifulSoup(a, 'html.parser')
for word in wanted:
    freq = soup.get_text().lower().count(word)
    dic = {'phrase': word, 'frequency': freq}
    fr.append(dic)
    print('Frequency of', word, 'is:', freq)
