import numpy as np
import pandas as pd
import itertools
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from newsapi import NewsApiClient
from newspaper import Article
import re
from detectiveNewsSystem import detectiveNewsSystem


class passiveAgressiveClassifier(detectiveNewsSystem):
    def splitting(mydata, ratio):
        mydata.shape
        mydata.head()
        labels=mydata.Label
        labels.head()
        return train_test_split(mydata['Body'], labels, test_size=ratio, random_state=7)




    def accuracy_rate(test, predictions):
        score=accuracy_score(test,predictions)
        print(f'Accuracy: {round(score*100,2)}%')


    def newsDetection (self,news):
        news = pd.DataFrame.from_records(news)
        if(news.size==0):return ([])
        pac=PassiveAggressiveClassifier(max_iter=50)
        df = pd.read_csv('d.csv',dtype='unicode')
        x_train,x_test,y_train,y_test = self.splitting (df,0.000001)
        tfidf_vectorizer=TfidfVectorizer(stop_words='english', max_df=0.7)
        tfidf_train=tfidf_vectorizer.fit_transform(x_train.values.astype('U'))
        pac.fit(tfidf_train,y_train.values.astype('U'))
        tfidf_detect=tfidf_vectorizer.transform(news[3].values.astype('U'))
        return pac.predict(tfidf_detect)



        





#####################################
Pac = passiveAgressiveClassifier;



#dns = detectiveNewsSystem

df2 = pd.read_excel('D:/Afnan/College/year 4/GP/passive detection.xlsx')

detect = df2.values.tolist()


pred= Pac.newsDetection(Pac,detect)
#pred= Pac.newsDetection(Pac,dns.getUndetectedNews())
#print (detect[3])
print(pred)

#Pac.accuracy_rate(y_test,y_pred)
