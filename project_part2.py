#!/usr/bin/env python
# coding: utf-8

# In[232]:


import matplotlib.pyplot as plt
import openpyxl
import pandas as pd
import re # regular expressions
import requests
import sys
import unidecode
from itertools import groupby
from operator import itemgetter
from bs4 import BeautifulSoup
from selenium import webdriver
from openpyxl.workbook import Workbook
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
URL = 'https://arbuz.kz/ru/almaty/catalog/cat/225161-moloko_syr_maslo_yaica#/'
driver.get(URL)
content = driver.page_source
soup = BeautifulSoup(content)


# installations: pip3 install openpyxl
# pip3 install xlwt 
# pip3 install unidecode
# pip install bs4
# pip install requests
# pip install seaborn
# 
# 

# In[233]:


#Getting product from one category
def FindItems(link,names,current_prices, previous_prices, discount_rates,has_discount,category_name,page_count):
    print(category_name)
    page=1
    while(page != page_count):
        r=requests.get(link).text
        soup=BeautifulSoup(r,"lxml") 
        block = soup.find('article', attrs={'class':'product-item product-card'})
        for block in soup.findAll('article', attrs={'class':'product-item product-card'}):
            name_str = block.find('a', attrs={'class': 'product-card__title'}).text.replace('\n','')
            current_price_str = block.find('p', attrs={'class': 'product-card__price'}).find('b').text.replace('\n','')
            previous_price_str = block.find('s', attrs={'class': 'product-card__price-previous'})
            current_price_str = unidecode.unidecode(current_price_str).replace(" ", "")
            current_price_str=current_price_str.replace('T', '')
            if(previous_price_str):
                previous_price_str = block.find('s', attrs={'class': 'product-card__price-previous'}).text.replace('\n','')
                previous_price_str = unidecode.unidecode(previous_price_str).replace(" ", "")
                previous_price_str=previous_price_str.replace('T', '')
            else:
                #in case product didn't had discount
                previous_price_str = current_price_str

            current_price_numb = int(current_price_str)
            previous_price_numb = int(previous_price_str)
            discount_rate_numb = 100 - (current_price_numb*100/previous_price_numb)
            names.append(name_str)
            current_prices.append(round(current_price_numb,2))
            previous_prices.append(round(previous_price_numb,2))
            discount_rates.append(int(discount_rate_numb))
            if(discount_rate_numb == 0):
                has_discount.append(False)
            else:
                has_discount.append(True)
            category_names.append(category_name)
        print("Getting page---",page,"---page") 
                
        page+=1


# In[234]:


#statistics
def Statistics(data):
    print("-----------------------------------------")
    print("------------Statistics-------------------")
    print("-----------------------------------------")
    average = sum(data['current_price'])/len(data['current_price'])
    print("Average of the prices =", round(average))
    average = sum(data['discount_rate'])/len(data['discount_rate'])
    print("Average of the discount rate =", round(average))
    print("The cheapest product =", min(data['current_price']))
    print("The most expensive product =", max(data['current_price']))
    print("The highest discount rate =", max(data['discount_rate']))
    df = pd.DataFrame(data)

    products = {}
    category_occurence = {}
    discount_occurence = {}
    category_price = {}
    for index, row in df.iterrows():
        category = row['name']
        category_list = category.split(" ")
        for word in category_list:
            products[word] = products.get(word, 0) + 1
        price = row['current_price']
        categories = row['category']
        discount = row['discount']
        if(discount):
            discount_occurence[categories] = discount_occurence.get(categories, 0) + 1
        category_occurence[categories] = category_occurence.get(categories, 0) + 1
        category_price[categories] = category_price.get(categories, 0) + price
  
    #prints how many products in each category
    print("-----------------------------------------")
    print("----Category and total product count-----")
    print("-----------------------------------------")
    
    
    for key in category_occurence:
        print("Total number "+key+" product: "+str(category_occurence[key]))
        
    print("-----------------------------------------")
    print("Category and total price of all products")
    print("-----------------------------------------")
    max_price = 0
    min_price = sys.maxsize
    max_key = "" 
    min_key = ""
    for key in category_price:
        print("Total price "+key+" product: "+f"{category_price[key]:,}"+" T")
        if(max_price<category_price[key]):
            max_price = category_price[key]
            max_key = key
        if(min_price > category_price[key]):
            min_price = category_price[key]
            min_key = key
    print("The most expensive category is: "+max_key+" and price "+f"{category_price[max_key]:,}"+" T")
    print("The most cheap category is: "+min_key+" and price "+f"{category_price[min_key]:,}"+" T")
    
    print("-----------------------------------------")
    print("Category and Discount occurence in that category")
    print("-----------------------------------------")   
    for key in discount_occurence:
        print("Total number "+key+" product: "+str(discount_occurence[key]))
        
    plt.hist(current_prices, bins=20)
    plt.title('Price Distribution')
    plt.xlabel('Prices')
    plt.show()
    

    


# In[235]:


names = []
current_prices = []
previous_prices = []
discount_rates = []
has_discount =[]
category_names = []
data = {
    'name': names,
    'current_price': current_prices,
    'price_after': previous_prices,
    'discount_rate': discount_rates,
    'discount': has_discount,
    'category': category_names
}

#Getting Milks
link = f"https://arbuz.kz/ru/almaty/catalog/cat/225161-moloko_syr_maslo_yaica#/?%5B%7B%22slug%22%3A%22page%22,%22value%22%3A={page}1,%22component%22%3A%22pagination%22%7D%5D"
FindItems(link,names,current_prices, previous_prices, discount_rates,has_discount,"Milk-Cheese-Eggs",34)

#Getting Drinks
link = f"https://arbuz.kz/ru/almaty/catalog/cat/14-napitki#/?%5B%7B%22slug%22%3A%22page%22,%22value%22%3A={page},%22component%22%3A%22pagination%22%7D%5D"
FindItems(link,names,current_prices, previous_prices, discount_rates,has_discount,"Drinks",47)

#Getting Fishes
link = f"https://arbuz.kz/ru/almaty/catalog/cat/225163-ryba_i_moreprodukty#/?%5B%7B%22slug%22%3A%22page%22,%22value%22%3A={page},%22component%22%3A%22pagination%22%7D%5D"
FindItems(link,names,current_prices, previous_prices, discount_rates,has_discount,"Fishes",11)

#Getting Vegetables and Fruits
link = f"https://arbuz.kz/ru/almaty/catalog/cat/225164-svezhie_ovoshi_i_frukty#/?%5B%7B%22slug%22%3A%22page%22,%22value%22%3A={page},%22component%22%3A%22pagination%22%7D%5D"
FindItems(link,names,current_prices, previous_prices, discount_rates,has_discount,"Vegtable-Fruit",13)

#Getting Cooking products
link = f"https://arbuz.kz/ru/almaty/catalog/cat/225253-kulinariya#/?%5B%7B%22slug%22%3A%22page%22,%22value%22%3A={page},%22component%22%3A%22pagination%22%7D%5D"
FindItems(link,names,current_prices, previous_prices, discount_rates,has_discount,"Cooking_products",9)

#Getting Fermer's products
link = f"https://arbuz.kz/ru/almaty/catalog/cat/225268-fermerskaya_lavka#/?%5B%7B%22slug%22%3A%22page%22,%22value%22%3A={page},%22component%22%3A%22pagination%22%7D%5D"
FindItems(link,names,current_prices, previous_prices, discount_rates,has_discount,"Fermers_products",11)

#Getting Bakery
link = f"https://arbuz.kz/ru/almaty/catalog/cat/225165-hleb_vypechka#/?%5B%7B%22slug%22%3A%22page%22,%22value%22%3A={page},%22component%22%3A%22pagination%22%7D%5D"
FindItems(link,names,current_prices, previous_prices, discount_rates,has_discount,"Bakery",4)

#Getting Meat
link = f"https://arbuz.kz/ru/almaty/catalog/cat/225162-myaso_ptica#/?%5B%7B%22slug%22%3A%22page%22,%22value%22%3A={page},%22component%22%3A%22pagination%22%7D%5D"
FindItems(link,names,current_prices, previous_prices, discount_rates,has_discount,"Meat",6)
print("Getting data is finished !!!!!")


# In[236]:


df = pd.DataFrame(data)
Statistics(data)


# In[237]:


df


# In[231]:


print("Dataset contains {} rows and {} columns".format(df.shape[0], df.shape[1]))
#writing data to xlsx file, since we don't need index we made it false
df.to_excel('data.xlsx', index=False)


# In[ ]:




