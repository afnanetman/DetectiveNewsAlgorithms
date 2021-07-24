import numpy as np
import pandas as pd
import itertools
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from detectiveNewsSystem import detectiveNewsSystem


   

class passiveAgressiveClassifier(detectiveNewsSystem):
    def splitting(mydata, ratio):
        #df.shape
        #df.head()
        labels=df.Label
        #labels.head()
        return train_test_split(mydata, labels, test_size=ratio, random_state=7) 



    def newsDetection (news):
        pac=PassiveAggressiveClassifier(max_iter=50)
        pac.fit(tfidf_train,y_train.values.astype('U'))
        return pac.predict(news)



    def accuracy_rate(test, predictions):
        score=accuracy_score(test,predictions)
        print(f'Accuracy: {round(score*100,2)}%')



        

df=pd.read_csv('d.csv',dtype='unicode')



#####################################
Pac = passiveAgressiveClassifier;

x_train,x_test,y_train,y_test = Pac.splitting (df['Body'],0.2)

tfidf_vectorizer=TfidfVectorizer(stop_words='english', max_df=0.7)

tfidf_train=tfidf_vectorizer.fit_transform(x_train.values.astype('U')) 
tfidf_test=tfidf_vectorizer.transform(x_test.values.astype('U'))


y_pred= Pac.newsDetection(tfidf_test)

Pac.accuracy_rate(y_test,y_pred)




    















