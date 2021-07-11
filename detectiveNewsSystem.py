import random
import csv
from newsapi import NewsApiClient
from newspaper import Article
import re
import pandas as pd
import datetime

class detectiveNewsSystem:
    
    def getUndetectedNews():
        mydata = []
        #filename = 'test.csv'
        #filename = 'test - Copy.csv'
        #mydata = csv.reader(open(filename, encoding='cp1252'))
        #api_key='edecbe9ce87b4205ad0cabf6ac7be55a'
        #api_key='c86583ceac0f421b8688f6bed011c94c'
        time =datetime.datetime.now() - datetime.timedelta(minutes=60*3)

        newsapi = NewsApiClient(api_key='ddd584655331475388eb27ed2de64898')
        categories = ['sports','politics','entertainment','technology','health','science','world']
        for x in range (len(categories)):
            all_articles = newsapi.get_everything(q=categories[x],language='en',from_param=time)

            print(x)
            articles = dict()
            articles = all_articles['articles']
            sources = newsapi.get_sources()
            df = pd.DataFrame(articles)
            
            for i in range (len(df.index)):
                data =[]
                try:
                    author = str(df['author'][i])
                    if(author !="None"):
                        data.append(author)   
                    else:
                        data.append("No Author")
                        
                    #data.append(re.split('T',df['publishedAt'][i])[0])
                    data.append(datetime.datetime.strptime(re.split('T',df['publishedAt'][i])[0],"%Y-%m-%d" ).strftime("%#d/%#m/%Y"))
        
                    data.append(df['title'][i])
        
                    url = df['url'][i]
                    article = Article(url) 
                    article.download()
                    article.parse()
                    data.append(article.text)

                    split_string = url.split("/", 3)
                    substring = split_string[0]+"//"+split_string[1]+split_string[2]
                    data.append(df['source'][i]['name'])

                    if(df['urlToImage'][i]!=""): data.append(1)
                    else: data.append(0)
                    data.append(categories[x])
                    if(len(data)!=0): mydata.append(data)
                    
                except : print('error')
                    
      
        print(mydata)
        print(len(mydata))
        
        return mydata
        
    
    ####def newsDetection fun

    #####insertion Fun

    
    

    def splitting(mydata, ratio): 
        train_num = int(len(mydata) * ratio) 
        train = [] 
        test = list(mydata) 
        while len(train) < train_num: 
            index = random.randrange(len(test))
            train.append(test.pop(index)) 
        return train, test


    def accuracy_rate(test, predictions): 
        correct = 0
        for i in range(len(test)): 
            if test[i][-1] == predictions[i]: 
                correct += 1
        return (correct / float(len(test))) * 100.0

    #getUndetectedNews()

    



