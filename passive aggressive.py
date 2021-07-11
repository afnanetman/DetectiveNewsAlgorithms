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


class passiveAgressiveClassifier(detectiveNewsSystem):
    def splitting(mydata, ratio):
        df.shape
        df.head()
        labels=df.Label
        labels.head()
        return train_test_split(mydata, labels, test_size=ratio, random_state=7) 



    def newsDetection (news): 
        pac=PassiveAggressiveClassifier(max_iter=50)
        pac.fit(tfidf_train,y_train.values.astype('U'))
        df=pd.read_csv('D:\\Afnan\\College\\year 4\\GP\\d.csv',dtype='unicode')
        x_train,x_test,y_train,y_test = splitting (df['Body'],0.000001)
        tfidf_vectorizer=TfidfVectorizer(stop_words='english', max_df=0.7)
        tfidf_train=tfidf_vectorizer.fit_transform(x_train.values.astype('U')) 
        tfidf_detect=tfidf_vectorizer.transform(news[3].values.astype('U'))


        return pac.predict(news)




    def accuracy_rate(test, predictions):
        score=accuracy_score(test,predictions)
        print(f'Accuracy: {round(score*100,2)}%')



        





#####################################
Pac = passiveAgressiveClassifier;



dns = detectiveNewsSystem
detect= pd.DataFrame.from_records(dns.getUndetectedNews())




pred= Pac.newsDetection(detect)
print (detect[3])
print(pred)

#Pac.accuracy_rate(y_test,y_pred)
