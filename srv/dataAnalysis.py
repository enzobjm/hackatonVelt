
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
from sklearn import tree

import pandas as pd
import matplotlib.pyplot as plt
import os
import json
import numpy as np


class DataAnalysis():
    def __init__(self):
        self.esgCache = {}
        self.glassDoorCache = {}
        self.RACache = {}
        self.kmeans = KMeans(n_clusters=6)
        self.knn = NearestNeighbors(n_neighbors=6)
        self.decisionTree = DecisionTreeClassifier()

    def loadFromCache(self):
        script_dir = os.path.dirname(__file__)
        with open(script_dir + '\\cache\\EsgCache.json') as json_file:
            self.esgCache = json.load(json_file)
        with open(script_dir + '\\cache\\GlassDoorCache.json') as json_file:
            self.glassDoorCache = json.load(json_file)
        with open(script_dir + '\\cache\\RACache.json') as json_file:
            self.RACache = json.load(json_file)
        
        esgArray = []
        for key in self.esgCache.keys():
            esgArray.append([key, self.esgCache[key]["Esg"]["rating"]])
        
        glassDoorArray = []
        for key in self.glassDoorCache.keys():
            glassDoorArray.append([key, float(self.glassDoorCache[key]["GlassDoor"]["Overall"]), float(self.glassDoorCache[key]["GlassDoor"]["Cultura_e_valores"]), float(self.glassDoorCache[key]["GlassDoor"]["Diversidade_e_inclusao"]), float(self.glassDoorCache[key]["GlassDoor"]["Qualidade_de_vida"]), float(self.glassDoorCache[key]["GlassDoor"]["Alta_lideranca"]), float(self.glassDoorCache[key]["GlassDoor"]["Remuneracao_e_beneficios"]), float(self.glassDoorCache[key]["GlassDoor"]["Oportunidades_de_carreira"])])
        
        raArray = []
        for key in self.RACache.keys():
            raArray.append([key, float(self.RACache[key]["RA"]["rating"]), float(self.RACache[key]["RA"]["Reclamacoes_respondidas"]), float(self.RACache[key]["RA"]["Voltariam_a_fazer_negocio"]), float(self.RACache[key]["RA"]["Indice_de_solucao"]), float(self.RACache[key]["RA"]["Nota_do_consumidor"])])
        
        self.esgFrame = pd.DataFrame(esgArray, columns=["Ticker", "EsgRating"])    
        self.glassDoorFrame = pd.DataFrame(glassDoorArray, columns=["Ticker", "Overall", "Cultura e Valores", "Diversidade e Inclusao", "Qualidade de Vida", "Alta Lideranca", "Remuneração e Beneficios", "Oportunidades de Carreira"])
        self.raFrame = pd.DataFrame(raArray, columns=["Ticker", "Rating", "Reclamacoes Respondidas", "Voltariam a Fazer Negócios", "Indice de Solucao", "Nota do Consumidor"])
        
        self.esgFrame.set_index("Ticker", inplace=True)
        self.glassDoorFrame.set_index("Ticker", inplace=True)
        self.raFrame.set_index("Ticker", inplace=True)

        self.finalFrame = pd.concat([self.esgFrame, self.glassDoorFrame, self.raFrame], axis=1)
        
        return self.finalFrame
    
    def kmeansFit(self, dataFrame):
        self.kmeans.fit(dataFrame)
        cluster_map = pd.DataFrame()
        cluster_map['data_index'] = dataFrame.index.values
        cluster_map['cluster'] =  self.kmeans.labels_
        return cluster_map

    def knnFit(self, dataFrame):
        self.knn.fit(dataFrame)
        result = self.knn.kneighbors([dataFrame.loc["ABEV3"]], return_distance=True)
        print(result)
        neighboursNames = []
        for key in result[1]:
            neighboursNames = dataFrame.index[key]
        return neighboursNames.values[1:]

    def decisionTreeESGClassifier(self, dataFrame):
        dataFrame = dataFrame[dataFrame.columns[:8]]

        print(dataFrame)
        size = len(dataFrame.values)
        test = dataFrame.iloc[0:19]
        train = dataFrame.iloc[19:]

        self.decisionTree.fit(train.loc[:, dataFrame.columns != "EsgRating"], train.loc[:, dataFrame.columns == "EsgRating"])
        predicted = self.decisionTree.predict(test.loc[:, dataFrame.columns != "EsgRating"])
        
        tree.export_graphviz(self.decisionTree,
                     out_file="tree.dot",
                     filled = True)
        print(test)
        print(predicted)
        print("Accuracy:",metrics.accuracy_score(predicted, test.EsgRating))


        

dataAnalysis = DataAnalysis()
dataAnalysis.loadFromCache()
notNullDF = dataAnalysis.finalFrame[dataAnalysis.finalFrame.EsgRating.notnull()][dataAnalysis.finalFrame.Rating.notnull()]

dataAnalysis.decisionTreeESGClassifier(notNullDF)
