from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from html.parser import HTMLParser

import pandas as pd
import json as json
import unidecode

class WebScraper():
    
    def __init__(self):
        chrome_options = Options()
        #chrome_options.add_argument("headless")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    def stop(self):
        self.driver.close()

    def getCompanyESGRating(self, companyId):
        self.driver.get('https://www.msci.com/esg-ratings/issuer' + companyId)
        content = self.driver.page_source

        soup = BeautifulSoup(content,features="lxml")
        esg = {}
        for rating in soup.findAll('div', attrs={'class':'ratingdata-container'}):
            rating = str(rating)
            esg["rating"] = self.evalRatingHtml(rating)

        for rating in soup.findAll('div', attrs={'class':'comparison-table row no-gutters'}):
            rating = str(rating)
            self.evalAspectsHtml(rating, esg)
        
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
        ra["empresa"] = companyId

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
        element = self.driver.find_element_by_class_name("css-1d56lwf")
        element.click()
        content = self.driver.page_source

        glassDoor = {}
        glassDoor["Empresa"] = companyId.split("-Avalia")[0]

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
