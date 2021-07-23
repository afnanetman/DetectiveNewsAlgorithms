import math 
import random 
import csv
import pandas as pd
from math import sqrt
from detectiveNewsSystem import detectiveNewsSystem

class naiveBaysClassifier(detectiveNewsSystem):
# class labels encoded to 0 , 1 
 def encode_class(self,mydata): 
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


 def splitting(self,mydata, ratio): 
    train_num = int(len(mydata) * ratio) 
    train = [] 
    test = list(mydata) 
    while len(train) < train_num: 
        index = random.randrange(len(test))
        train.append(test.pop(index)) 
    return train, test


# Group data rows under each class dict[unacc], dict[acc], dict[vgood] & dict[good]
 def groupUnderClass(self,mydata): 
      dict = {} 
      for i in range(len(mydata)): 
          if (mydata[i][-1] not in dict): 
              dict[mydata[i][-1]] = [] 
          dict[mydata[i][-1]].append(mydata[i]) 
      return dict

 def accuracy_rate(self,test, predictions): 
    correct = 0
    for i in range(len(test)): 
        if test[i][-1] == predictions[i]: 
            correct += 1
    return (correct / float(len(test))) * 100.0  


#----------------------code----------------------
 def newsDetection(self):
  filename = 'news_articles3WithoutColNames_withNewArticles.csv'
  mydata = csv.reader(open(filename, encoding='cp1252'))
  mydata = list(mydata)
  mydata , classes = self.encode_class(mydata) 
  ratio = 0.75
  train_data, test_data = self.splitting(mydata, ratio) 

#*****************************-Learn Phase-******************************


  classesDic = dict()


  for i in range(len(train_data[0])-1):
    arr=[]
    for j in range(len(train_data)):
        if train_data[j][i] not in arr:
            arr.append(train_data[j][i])
    classesDic[i]= arr

  groupClass=dict()
  groupClass=self.groupUnderClass(train_data)    
  pC=dict()

  for i in range (len(groupClass)):
    for key in groupClass:
        pC[key]=(len(groupClass[key])/len(train_data))


  clist=dict()
  predictions=[]
  while(True):
     for i in range(len(train_data[0])-1):
        valueRange = [] 
        for j in range(len(train_data)):
            if train_data[j][i] not in valueRange: 
                valueRange.append(train_data[j][i])    
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


#*****************************-Test Phase-******************************
  for i in range(len(test_data)):
    prob=dict()
    for key in groupClass:
       p=pC[key]
       for j in range(len(test_data[0])-1):
            string=str(key)+'-'+str(j)+'-'+str(test_data[i][j])
            if string in clist.keys(): p*=clist[string]
       prob[key]=p
    
    predictions.append(max(prob,key=prob.get))

#--------accuracey-------------

  accuracy = self.accuracy_rate(test_data, predictions) 
  print("Accuracy is: ", accuracy)
 
class_instance = naiveBaysClassifier()
class_instance.newsDetection()

