import pandas as pd    
import matplotlib.pyplot as plt
from pytrends.request import TrendReq

class WebRequest():

    def __init__(self):
        self.pytrend = TrendReq(hl='pt-BR')

    
    def getGoogleSearchTrend(self, company):
        self.pytrend.build_payload(company, cat=0, geo='', gprop='')
        df = self.pytrend.interest_over_time()
        df.reset_index(level=0, inplace=True)
        historical = {}
        historical["historical"] = df.values.tolist()
        return historical
    
    def getGoogleRelated(self, company):
        self.pytrend.build_payload(company, cat=0, geo='', gprop='')
        relatedQueries = self.pytrend.related_queries()
        print(relatedQueries)
        return relatedQueries
    


