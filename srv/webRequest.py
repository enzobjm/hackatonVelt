import pandas as pd    
import matplotlib.pyplot as plt
from pytrends.request import TrendReq

class WebRequest():

    def __init__(self):
        self.pytrend = TrendReq(hl='pt-BR')

    
    def getSearchTrend(self, company):
        self.pytrend.build_payload(company, cat=0, geo='', gprop='')
        df = self.pytrend.interest_over_time()
        return df
    
    def getRelated(self, company):
        self.pytrend.build_payload(company, cat=0, geo='', gprop='')
        relatedQueries = self.pytrend.related_queries()
        return relatedQueries
    


