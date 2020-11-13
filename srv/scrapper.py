from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from html.parser import HTMLParser

import pandas as pd

class WebScrapper():
    
    def __init__(self):
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)


    def getCompanyESGRating(self, companyId):
        self.driver.get('https://www.msci.com/esg-ratings/issuer' + companyId)
        print(companyId)
        content = self.driver.page_source

        soup = BeautifulSoup(content,features="lxml")
        esg = {}
        for rating in soup.findAll('div', attrs={'class':'ratingdata-container'}):
            rating = str(rating)
            esg["rating"] = self.evalRatingHtml(rating)
            print(esg)
        for rating in soup.findAll('div', attrs={'class':'comparison-table row no-gutters'}):
            rating = str(rating)
            self.evalAspectsHtml(rating)

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

    def evalAspectsHtml(self, hmtlString):
        columns = hmtlString.split("comparison-body row no-gutters justify-content-center")
        for i in range(1, len(columns)):
            if(i == 1):
                print("LAGGARD:")
            elif(i == 2):
                print("AVERAGE:")
            else:
                print("LEADING:")
            if("span" in columns[i]):
                content = columns[i].split("span")
                for j in range(1, len(content), 2):
                    print(content[j])
        
scrapper = WebScrapper()
scrapper.getCompanyESGRating("/petroleo-brasileiro-sa-petrobras-/IID000000002179425")
scrapper.getCompanyESGRating("/itau-unibanco-holding-sa/IID000000002257223")