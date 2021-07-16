from flask import Flask, jsonify, request
import json
from passiveAggressive import passiveAgressiveClassifier 

#declared an empty variable for reassignment
response = ''

#creating the instance of our flask application
app = Flask(__name__)

#route to entertain our post and get request from flutter app
@app.route('/article', methods =['POST'])
def nameRoute():

    #fetching the global response variable to manipulate inside the function
    global response

    #checking the request type we get from the app
    request_data = request.data #getting the response data
    request_data = json.loads(request_data.decode('utf-8')) #converting it from json to key value pair
    article = request_data['article'] #assigning it to name
    print(article)
    news=[['null','null','null',article]]
    Pac = passiveAgressiveClassifier
    result = Pac.newsDetection(Pac,news)
    print(result[0])
    #response = print(result[0]) #re-assigning response with the name we got from the user
    return jsonify({'article' : result[0]}) #sending data back to your frontend app

if __name__ == "__main__":
    app.run(debug=True)
