import math
import random
import csv
from math import sqrt
import schedule
import time
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
        classes = [] 
        for i in range(len(mydata)): 
            if mydata[i][-1] not in classes: 
                classes.append(mydata[i][-1])
        labelSize=len(classes)
        for i in range(len(classes)): 
            for j in range(len(mydata)): 
                if mydata[j][-1] == classes[i]: 
                    mydata[j][-1] = i 
        return mydata ,classes
    
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
            for i in range(len(data[0])-1):
                valueRange = [] 
                for j in range(len(data)):
                    if data[j][i] not in valueRange: 
                        valueRange.append(data[j][i])    
                for key in groupClass:
                         for x in range(0,len(valueRange)):
                             ctr=0
                             cString = ''
                             for j in range(0,len(groupClass[key])):
                                 if(valueRange[x]==groupClass[key][j][i]):
                                     ctr+=1                 
                             cString = str(key)+'-'+str(i)+'-'+valueRange[x]
                             clist[cString]= ctr/len(groupClass[key])

        #_____________________ if probability = 0 ________________________

            N=0
            for key in clist:
                if (clist[key]==0):
                    classLabel=key[0]
                   
                    row=key[2]
            
                    clist[key]=1/(len(groupClass[int(classLabel)])+len(classesDic.get(int(row))))
                    for key in clist:                
                        if (key[0]==(classLabel)):
                            clist[key]=((clist[key]*len(groupClass[int(classLabel)]))+1)/(len(groupClass[int(classLabel)])+len(classesDic.get(int(row))))
            for key in clist:
                if (clist[key]==0):N=1
            if (N==0):break
        
        return clist

   

    def newsDetection(self):
        #----------------------code----------------------
        #filename = 'news_articles3WithoutColNames.csv'
        #filename = 'news_articles3WithoutColNames - Copy.csv'#wa5da test data mn train
        filename = 'news_articles3WithoutColNames_withNewArticles.csv'
        mydata = csv.reader(open(filename, encoding='cp1252'))
        mydata = list(mydata)
        mydata , classes = self.encode_class(mydata)
        undetectedNews={}
        undetectedNews = detectiveNewsSystem.getUndetectedNews()

        classesDic = dict()


        for i in range(len(mydata[0])-1):
            arr=[]
            for j in range(len(mydata)):
                if mydata[j][i] not in arr:
                    arr.append(mydata[j][i])
            classesDic[i]= arr
            
       # Group data rows under each class dict[fake], dict[real]
        groupClass=dict() 
        groupClass= self.groupUnderClass(mydata)
          
        pC=dict()
        pC= self.labelsProb(groupClass , len(mydata))

        clist=dict()
              
        clist = self.dataProb (mydata, groupClass , classesDic)



        #*****************************-Detection-******************************
        passiveAgressive=[]
        predictions=[]
        detection=[]
        detectedData=[]
        po=[]
        
        #print ('undetectedNews  lengthhhh : ' ,  len(undetectedNews))         
        
        for i in range(len(undetectedNews)):
            prob=dict()
            for key in groupClass:
               p=pC[key]
               for j in range(len(undetectedNews[0])-2):
##                    print ('undetectedNews  lengthhhh : ' ,  len(undetectedNews))
##                    print ('len(undetectedNews[0])-1 : ' , len(undetectedNews[0])-1)         


                    string=str(key)+'-'+str(j)+'-'+str(undetectedNews[i][j])
                    if string in clist.keys(): p*=clist[string]
               prob[key]=p
               
            precentage = ( prob[max(prob,key=prob.get)]/(prob[0]+prob[1]))
            po.append(precentage)
            #if (prob[0]==prob[1]):
            if (precentage<0.6):
                print(prob)
                print("^^^^^^precentage^^^^^^^^^^",precentage)
                print('******************* passive agressive ***************************')
                passiveAgressive.append(undetectedNews[i])
                ########################################
    
                predictionDecode=self.decode_class(max(prob,key=prob.get))
                print(predictionDecode)
                detection.append(predictionDecode)
                
            else:
                
                #predictions.append(max(prob,key=prob.get))
                #precentage = ( prob[max(prob,key=prob.get)]/(prob[0]+prob[1]))
                print(prob[0] , prob[1])
                print("max" , prob[max(prob,key=prob.get)])
                print("prop",prob)
         #       print(undetectedNews[i])
                predictionDecode=self.decode_class(max(prob,key=prob.get))
                print(predictionDecode)
                print("^^^^^^precentage^^^^^^^^^^",precentage)
                detection.append(predictionDecode)
                # detectedArticle.append(undetectedNews[i])
                #detectedArticle.append(detection[i])
                #detectedArticle.append(precentage)
                #detectedArticle.append(undetectedNews[i][6])
                undetectedNews[i].append(predictionDecode)
                #undetectedNews[i].append(precentage)
                detectedData.append(undetectedNews[i])

        print ('undetectedNews  lengthhhh after loooooooooop : ' ,  len(undetectedNews))         

       # print(' detected Data *************************** :  ' ,detectedData )
        print ('detectedData  lengthhhh : ' ,  len(detectedData))
        
        #print(' passive agressive *************************** :  ' ,passiveAgressive )
        print ('passiveAgressive  lengthhhh : ' ,  len(passiveAgressive))


        if (len(passiveAgressive)>0):
            print('================= PASSIVE AGREZZZZZZIVVVEEE =============')
            news=passiveAgressiveClassifier

            passiveAgressiveDetction=news.newsDetection(news,passiveAgressive)
            print('passiveAgressiveDetction ',passiveAgressiveDetction)
            for i in range(len(passiveAgressive)):
                 passiveAgressive[i].append(passiveAgressiveDetction[i])
                 detectedData.append(passiveAgressive[i])
                 #detectedData.appentd(passiveAgressive[i])
                 #detectedData.appentd(passiveAgressiveDetction[i])
                 #detectedData.appentd(passiveAgressive[i][6])
                
        print('********************* laaaaaaaaaaaaaaaaaaassssssssssttttt *************************** :  ' )       
        #print(' Neww detected Data *************************** :  ' ,detectedData )
        print ('detectedData  lengthhhh : ' ,  len(detectedData))         
        print(detection)
        print(po)
            
            
    #############################3
        #####***********INSERT TO DB (detectedData)
        
        detectiveNewsSystem.FireBaseInsert(detectedData)

        #return detection


class_instance = naiveBaysClassifier()
class_instance.newsDetection()

#schedule.every(10).minutes.do(class_instance.newsDetection())

#print(class_instance.newsDetection())
#print(schedule.every(10).minutes.do(naiveBaysClassifier()).newsDetection())
#schedule.every(1).minutes.do(class_instance.newsDetection)
#schedule.every().hour.do(class_instance.newsDetection)
schedule.every(3*60).minutes.do(class_instance.newsDetection)
while True:
    schedule.run_pending()
    time.sleep(1)
    #print('*****************************************')


