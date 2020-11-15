# Sancho Server

Sancho Server is a Web Scraper, Handler and Analisys Central for data from main public available data, such as Reclame Aqui, Glassdoor, MSCI, Google and Twitter. Almost all data is being scraped from web pages. 
There is also Cache Files for Reclame Aqui, Glassdoor and MSCI data, collected on 15/11/2020, that is the default data source for the implemted Machine Learning and Clusterization Algorithms, such as KNN, KMeans and Decision Tree Classifier.
Further data management and the implementation of the proposed REST API will be completed in the next phase of the project.
At srv/Links.csv, you can find the default links used as function paramethers for any scraping to GlassDoor, Reclame Aqui and MSCI.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to get all packages.

```bash
pip install numpy
pip install -U scikit-learn
pip install pandas
pip install matplotlib
pip install pytrends
pip install selenium
pip install bs4
pip install webdriver-manager
```

## WebRequest Class
This class should be used for Google Trends Requests

```python
import WebRequests

requests = WebRequests()
requests.getGoofleSearchTrend(["ITAU"]) #Returns last 5 years trends for ITAU on Google
requests.getGoogleRelared(["ITAU"]) #Return list of related queries for ITAU on Google

```

## Scraper Class
This class should be used to fetch data from Reclame Aqui, GlassDoors, MSCI ESG Ratings and Twitter.

```python
import WebScraper

scraper = WebScraper()
scraper.getCompanyESGRating("itau-unibanco-holding-sa/IID000000002257223") # Returns MSCI ESG Rating for Itau
scraper.getRARating("itau") # Returns Reclame Aqui data for Itau
scraper.getGlassDoorRating("Ita%C3%BA-Unibanco-Ita%C3%BA-BBA-e-Rede-Avalia%C3%A7%C3%B5es-E10999.htm") #Returns GlassDoors data for Itau
scraper.getTwitterTimestamps("Itau") #Get list with timestamps for newest posts containing Itau on it.

```

## Data Analysis Class
This class should be used to run data train, test and model fit for colected and requested data. 

```python
import DataAnalysis

analysis = DataAnalysis()
dataAnalysis.loadFromCache() #Loading previous requested data

notNullDF = dataAnalysis.finalFrame[dataAnalysis.finalFrame.EsgRating.notnull()]
notNullDF = notNullDF[dataAnalysis.finalFrame.Rating.notnull()] #Filtering for only non null data

analysis.kmeansFit(notNullDF) #Will return the list of Clusters and Companies that composes it
analysis.knnFit(notNullDF, "ITUB4") #Will return the list of 5 Companies that are most related with ITAU

analysis.decisionTreeESGClassifier(notNullDF) #Will train and test the Decision Tree model to assert ESG ratings from Reclame Aqui and GlassDoors ratings

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
