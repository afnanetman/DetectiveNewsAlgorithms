import math
import random
import csv
from math import sqrt
import schedule
import time
from newsapi import NewsApiClient
from newspaper import Article
import re
import pandas as pd
import datetime
import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore
import insert 
from detectiveNewsSystem import detectiveNewsSystem
from passiveAggressive import passiveAgressiveClassifier 



class naiveBaysClassifier(detectiveNewsSystem):
    
    def splitting(self, mydata, ratio): 
        train_num = int(len(mydata) * ratio) 
        train = [] 
        test = list(mydata) 
        while len(train) < train_num: 
            index = random.randrange(len(test))
            train.append(test.pop(index)) 
        return train, test

    def accuracy_rate(self, test, predictions): 
        correct = 0
        for i in range(len(test)): 
            if test[i][-1] == predictions[i]: 
                correct += 1
        return (correct / float(len(test))) * 100.0
    
    # class labels encoded to 0 , 1
    def encode_class(self , mydata): 
            for j in range(len(mydata)): 
                if mydata[j][-1] == 'Real': 
                    mydata[j][-1] = 0
                else: mydata[j][-1] = 1
            return mydata 
    
    # class labels decode to REAL , FAKE
    def decode_class(self , prediction):
        
       # for i in prediction:
            if (prediction == 0):detection = 'REAL'
            else:detection = 'FAKE'
            return detection
    
    # Group data rows under each class dict[fake], dict[real]
    def groupUnderClass(self,mydata): 
      dict = {} 
      for i in range(len(mydata)): 
          if (mydata[i][-1] not in dict): 
              dict[mydata[i][-1]] = [] 
          dict[mydata[i][-1]].append(mydata[i]) 
      return dict

    #getting data from news API
    def getUndetectedNews(self):
            mydata = []
            #api_key='edecbe9ce87b4205ad0cabf6ac7be55a'
            #api_key='c86583ceac0f421b8688f6bed011c94c'
            #ddd584655331475388eb27ed2de64898
            time =datetime.datetime.now() - datetime.timedelta(minutes=60*3)
        
            newsapi = NewsApiClient(api_key='c86583ceac0f421b8688f6bed011c94c')
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
                        
                    #   data.append(re.split('T',df['publishedAt'][i])[0])
                        data.append(datetime.datetime.strptime(re.split('T',df['publishedAt'][i])[0],"%Y-%m-%d" ).strftime("%#d/%#m/%Y"))
            
                        data.append(df['title'][i])
        
                        url = df['url'][i]
                        article = Article(url) 
                        article.download()
                        article.parse()
                        data.append(article.text)

##                        split_string = url.split("/", 3)
##                        substring = split_string[0]+"//"+split_string[1]+split_string[2]
                        data.append(df['source'][i]['name'])

                        if(df['urlToImage'][i]!=""): data.append(1)
                        else: data.append(0)
                        data.append(categories[x])
                        data.append(df['urlToImage'][i])
                        if(len(data)!=0): mydata.append(data)
                    
                    except : print('error')
                    
      
##            print(mydata)
            print(len(mydata))
        
            return mydata

    #insert to firbase
    def FireBaseInsert(self,mydata):

            for i in range (len(mydata)):
                data = [{'Author':mydata[i][0],'Date':mydata[i][1],'Title':mydata[i][2],'Content':mydata[i][3],'Source':mydata[i][4],'Category':mydata[i][6],'Image':mydata[i][7],'Label':mydata[i][8]}]
                headers = ['Author','Date','Title','Content','Source','Category','Label','Image']
                data_types = ['string','string','string','string','string','string','string','string']

                for batched_data in insert.batch_data(data, 499):
                    batch = insert.store.batch()
                    for data_item in batched_data:
                        doc_ref = insert.store.collection(insert.collection_name).document()
                        batch.set(doc_ref, data_item)
                    batch.commit()
        


###########################code fun############################
    
    def labelsProb(self , groupClass , dataLen):
         pC=dict()
         for i in range (len(groupClass)):
            for key in groupClass:
                pC[key]=(len(groupClass[key])/dataLen)
         return pC;

   ####################################################

    def dataProb (self , data , groupClass , classesDic):
        
        clist=dict()
        predictions=[]
        while(True):
            for i in range(len(data[0])-1): #3dad col - class label =(6)
                valueRange = [] 
                for j in range(len(data)):
                    if data[j][i] not in valueRange: 
                        valueRange.append(data[j][i])    #ba7ot feh distinct values ely f kol col ex: valueRange=['100percentfedup', 'BBC News'] valueRange=['1']
                for key in groupClass:
                         for x in range(0,len(valueRange)):
                             ctr=0
                             cString = ''
                             for j in range(0,len(groupClass[key])):
                                 if(valueRange[x]==groupClass[key][j][i]): 
                                     ctr+=1                 #count kam mara distinct value d at3mlt m3 real / fake
                             cString = str(key)+'-'+str(i)+'-'+valueRange[x] #(0/1 - col - distinct value)
                             clist[cString]= ctr/len(groupClass[key])

        #_____________________ if probability = 0 ________________________

            N=0
            for key in clist:
                if (clist[key]==0):
                    classLabel=key[0] #b7ot class label bta3 l distinct value ely prob bt3to = 0
                                      #key = '0-0-'BBC News''
                   
                    row=key[2] #bashoof hwa f anie row
            
                    clist[key]=1/(len(groupClass[int(classLabel)])+len(classesDic.get(int(row)))) #b3d ma deft 1 lel attribute ely kan prob = 0 w 7sbtalo prob
                    for key in clist:                
                        if (key[0]==(classLabel)): #ha3ml update lel probs ely mwgden f nfs row 
                            clist[key]=((clist[key]*len(groupClass[int(classLabel)]))+1)/(len(groupClass[int(classLabel)])+len(classesDic.get(int(row))))
            for key in clist: #check law feh prob = 0 tany 3shan a3rf a5rog mn while
                if (clist[key]==0):N=1
            if (N==0):break
        
        return clist

   

    def newsDetection(self):
        #----------------------code----------------------
        filename = 'news_articles3WithoutColNames_withNewArticles.csv'
        mydata = csv.reader(open(filename, encoding='cp1252'))
        mydata = list(mydata)
        #mydata , classes = self.encode_class(mydata)
        mydata = self.encode_class(mydata)
        undetectedNews={}
        undetectedNews = self.getUndetectedNews()

        classesDic = dict()


        for i in range(len(mydata[0])-1):
            arr=[]
            for j in range(len(mydata)):
                if mydata[j][i] not in arr:
                    arr.append(mydata[j][i])
            classesDic[i]= arr #col distinct value  ex: {0:['CNN','BBC'],...5:['1']}
            
       # Group data rows under each class dict[fake], dict[real] ex: {0: [['Barracuda Brigade','10/26/2016',..],[]],1:[[....]]}
        groupClass=dict() 
        groupClass= self.groupUnderClass(mydata)
          
        pC=dict()
        pC= self.labelsProb(groupClass , len(mydata))

        clist=dict()
              
        clist = self.dataProb (mydata, groupClass , classesDic) #{'0-0-Barracuda Brigade': 0.09523809523809523, '0-0-https://www.facebook.com/bbcnews': 0.14285714285714285, '0-0-No Author': 0.42857142857142855, '1-0-Barracuda Brigade': 0.3125, '1-0-https://www.facebook.com/bbcnews': 0.5, '1-0-No Author': 0.25,
                                                                #'0-1-10/26/2016': 0.09523809523809523, '0-1-6/26/2021': 0.09523809523809523, '0-1-6/10/2021': 0.14285714285714285, '0-1-6/21/2021': 0.09523809523809523, '0-1-6/13/2021': 0.09523809523809523, '0-1-6/8/2021': 0.09523809523809523, '0-1-7/6/2021': 0.14285714285714285, '0-1-6/20/2021': 0.09523809523809523, '0-1-7/2/2021': 0.07256235827664399, '0-1-7/8/2021': 0
                                                                # byaymshy 3la kol col w yeshoof prob bta3 kol attribute f col da ama ykon m3 0 aw 1
                                                                #(Real-col index - Barracuda Brigade': prob)


        #*****************************-Detection-******************************
        passiveAgressive=[]
        predictions=[]
        #detection=[]
        detectedData=[]
        po=[]
                
        for i in range(len(undetectedNews)):
            prob=dict()
            for key in groupClass: 
               p=pC[key]
               for j in range(len(undetectedNews[0])-2):

                    string=str(key)+'-'+str(j)+'-'+str(undetectedNews[i][j])
                    if string in clist.keys(): p*=clist[string] #check law l value ely gyaly d mawgooda f excel 3ndy 
               prob[key]=p
               
            precentage = ( prob[max(prob,key=prob.get)]/(prob[0]+prob[1]))
            po.append(precentage)
            if (prob[0]==prob[1]):
                passiveAgressive.append(undetectedNews[i])
                #predictionDecode=self.decode_class(max(prob,key=prob.get))
                #detection.append(predictionDecode)
                
            else:
                predictionDecode=self.decode_class(max(prob,key=prob.get))
                #detection.append(predictionDecode)
                undetectedNews[i].append(predictionDecode)
                detectedData.append(undetectedNews[i])

        print ('detectedData  lengthhhh : ' ,  len(detectedData))
        print ('passiveAgressive  lengthhhh : ' ,  len(passiveAgressive))


        if (len(passiveAgressive)>0):
            print('================= PASSIVE AGREZZZZZZIVVVEEE =============')
            news=passiveAgressiveClassifier
            passiveAgressiveDetction=news.newsDetection(news,passiveAgressive)
            print('passiveAgressiveDetction ',passiveAgressiveDetction)
            for i in range(len(passiveAgressive)):
                 passiveAgressive[i].append(passiveAgressiveDetction[i])
                 detectedData.append(passiveAgressive[i])
                
                
        print('********************* laaaaaaaaaaaaaaaaaaassssssssssttttt *************************** :  ' )       
        print ('detectedData  lengthhhh : ' ,  len(detectedData))         
        #print(detection)
        print(po)
  
        self.FireBaseInsert(detectedData)
        print('Done')


class_instance = naiveBaysClassifier()
class_instance.newsDetection()
schedule.every(3*60).minutes.do(class_instance.newsDetection)
while True:
    schedule.run_pending()
    time.sleep(1)


