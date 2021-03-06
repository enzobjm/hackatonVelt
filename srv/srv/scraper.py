from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from html.parser import HTMLParser

import pandas as pd
import json as json
import unidecode
import time

class WebScraper():
    
    def __init__(self):
        chrome_options = Options()
        #chrome_options.add_argument("headless")

        chrome_options.add_argument("--user-data-dir=C:\\Users\\Enzo Bustamante\\AppData\\Local\\Google\\Chrome\\User Data")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    def stop(self):
        self.driver.close()

    def getCompanyESGRating(self, companyId):
        self.driver.get('https://www.msci.com/esg-ratings/issuer/' + companyId)
        time.sleep(4)

        content = self.driver.page_source

        soup = BeautifulSoup(content,features="lxml")
        esg = {}

        for rating in soup.findAll('div', attrs={'class':'ratingdata-container'}):
            rating = str(rating)

            esg["rating"] = self.evalRatingHtml(rating)

        return esg

    def evalRatingHtml(self, hmtlString):
        if("esg-rating-circle-ccc\"" in hmtlString):
            return "CCC"
        elif("esg-rating-circle-b\"" in hmtlString):
            return "B"
        elif("esg-rating-circle-bb\"" in hmtlString):
            return "BB"
        elif("esg-rating-circle-bbb\"" in hmtlString):
            return "BBB"
        elif("esg-rating-circle-a\"" in hmtlString):
            return "A"
        elif("esg-rating-circle-aa\"" in hmtlString):
            return "AA"
        elif("esg-rating-circle-aaa\"" in hmtlString):
            return "AAA"
        else:
            return"Not Available"

    def evalAspectsHtml(self, hmtlString, esg):
        columns = hmtlString.split("comparison-body row no-gutters justify-content-center")
        for i in range(1, len(columns)):
            if(i == 1):
                key = "laggard"
            elif(i == 2):
                key = "average"
            else:
                key = "leading"
            esg[key] = []
            if("span" in columns[i]):
                content = columns[i].split("span")
                for j in range(1, len(content), 2):
                    esg[key].append(content[j][1:-2])
    
    def getRARating(self, companyId):
        self.driver.get('https://www.reclameaqui.com.br/empresa/' + companyId)
        content = self.driver.page_source
        soup = BeautifulSoup(content,features="lxml")
        ra = {}

        for rating in soup.findAll('span', attrs={'class':'score'}):
            try:
                value = rating.select_one('b').text.strip()
                ra["rating"] = value
            except:
                print("Key Not Found")
                
        soup = soup.findAll('div', attrs={'class':'sc-jDwBTQ dbRhhQ'})[0]
        keys = []
        for key in soup.findAll('p'):
             keys.append(unidecode.unidecode(key.text.strip().replace(" ", "_")))

        values = []
        for value in soup.findAll('span'):
             values.append(unidecode.unidecode(value.text.strip().replace(" ", "_")))

        for key, value in zip(keys, values):
            ra[key] = value

        return ra
       
    
    def getGlassDoorRating(self, companyId):
        self.driver.get('https://www.glassdoor.com.br/Avalia%C3%A7%C3%B5es/' + companyId)
        self.driver.find_element_by_class_name("v2__EIReviewsRatingsStylesV2__ratingInfo").click()
        content = self.driver.page_source
        glassDoor = {}

        soup = BeautifulSoup(content,features="lxml")
        keys = ["Overall"]

        for key in soup.findAll('div', attrs={'class':'col-6 p-0'}):
            keys.append(unidecode.unidecode(key.text.strip().replace(" ", "_")))
        
        values = []
        for value in soup.findAll('div', attrs={'class':'col-2 p-0 eiRatingTrends__RatingTrendsStyle__ratingNum'}):
            values.append(value.text.strip())

        for key, value in zip(keys, values):
            glassDoor[key] = value
        
        return glassDoor

    def getFundamenteiLinks(self, ticker):
        self.driver.get('https://fundamentei.com/br/' + ticker)
        content = self.driver.page_source
        soup = BeautifulSoup(content,features="lxml")
        sites = {}
        for value in soup.findAll('a', attrs={'class':'css-e08q0q'}):
            if(value.text.strip() == "Reclame Aqui" or value.text.strip() == "Glassdoor"):
                sites[value.text.strip().replace(" ", "")] = value["href"]
        
        return sites

    def getTwitterTimestamps(self, ticker):
        self.driver.get("https://twitter.com/search?q=" + ticker + "&src=typeahead_click&f=live")
        time.sleep(8)

        content = self.driver.page_source
        soup = BeautifulSoup(content, features="lxml")
        tweets = {}
        tweets["ticker"] = ticker
        tweets["timestamps"] = []
            
        for timestamp in soup.findAll('time'):
            tweets["timestamps"].append(timestamp.attrs['datetime'])
        
        return tweets
