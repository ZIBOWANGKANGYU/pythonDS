# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 19:42:06 2019

@author: kangyuwang

This file creates a game based on data from *quotes to scrape* website.
"""
import pickle
import requests
from bs4 import BeautifulSoup
import csv
import random

# Create classes and functions
## Create the quote class
class quote:
    def __init__(self, text, author_name, tags, link, author=None):
        self.text=text
        self.author_name=author_name
        self.tags=tags
        self.author_link="http://quotes.toscrape.com"+link
    def round_1(self):
        print(self.text)
        ans=input("Who said this? Please input name:\n")
        if ans==self.author_name:
            print("Congratulations! You are correct!")
        else:
            return self.round_2()
    def round_2(self):
        print(f"Your answer is not correct. Please see the additional information:\nThe person is born on {self.author.birthday}.")
        ans=input("Who said this? Please input name:\n")
        if ans==self.author_name:
            print("Congratulations! You are correct!")
        else:
            return self.round_3()
    def round_3(self):
        print(f"Your answer is not correct. Please see the additional information:\nThe person is born in {self.author.location}.")
        ans=input("Who said this? Please input name:\n")
        if ans==self.author_name:
            print("Congratulations! You are correct!")
        else:
            return self.round_4()
    def round_4(self):
        quotes_copy=quotes[:]
        quotes_copy.remove(self)
        sample=random.choices(quotes_copy, k=3)
        sample_names=[quote.author_name for quote in sample]
        sample_names.append(self.author_name)
        sample_names.sort()
        options_letter=["A", "B", "C", "D"]
        options = {options_letter[i]: sample_names[i] for i in range(len(sample_names))} 
        print(f"Your answer is not correct. Please choose one among the four alternatives: {options}")
        ans=input("Who said this? Please input A, B, C or D:\n")
        while ans not in options_letter:
            ans=input("please input a letter, A, B, C or D:\n")
        if options[ans]==self.author_name:
            print("Congratulations! You are correct!")
        else:
            print("You failed!")
        
## Create the author_info class
class author_info:
    def __init__(self, name, birthday, location, info):
        self.name=name
        self.birthday=birthday
        self.location=location
        self.info=info
## Create functions
def author_info_get(link):
        raw=requests.get(link)
        return BeautifulSoup(raw.text)
    
def next_page(page_url):
            link=BeautifulSoup(requests.get(page_url).text).find_all(class_="next")[0].find_all(attrs={"href": True})[0]["href"]
            return "http://quotes.toscrape.com"+link
        
def quote_combiner(initial_page_url):
    page_url=initial_page_url
    quotes=BeautifulSoup(requests.get(initial_page_url).text).find_all(class_="quote")
    while True:
        try:
            page_url=next_page(page_url)
            quotes=quotes+BeautifulSoup(requests.get(page_url).text).find_all(class_="quote")
        except IndexError:
            return quotes

#Read in data
with open('data.pkl', "rb") as f:
    quotes, author_info_class = pickle.load(f)

#Randomize the quotes list
random.shuffle(quotes)
#Name of the player
name_player=input("Please input your name:\n")
print(f"{name_player}, Welcome to the game!")
#The game
continue_game="Y"
i=0
while continue_game=="Y": 
    quotes[i].round_1()
    continue_game=input("Do you want to continue the game? Y or N\n")
    i=i+1
    




