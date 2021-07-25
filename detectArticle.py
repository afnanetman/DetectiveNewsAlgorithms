from flask import Flask, jsonify, request
import json
from passiveAggressive import passiveAgressiveClassifier 

#creating the instance of our flask application
app = Flask(__name__)

#route to entertain our post request from flutter app
@app.route('/article', methods =['POST'])
def nameRoute():

    request_data = request.data #getting the article
    request_data = json.loads(request_data.decode('utf-8')) #converting it from json to key value pair {'article': 'input article from flutter'}
    article = request_data['article'] #assign Key of article to article variable
    print(article)
    news=[['null','null','null',article]]
    Pac = passiveAgressiveClassifier
    result = Pac.newsDetection(Pac,news)
    print(result[0])
    return jsonify({'article' : result[0]}) #sending data back to your frontend app {'article' : fake / real} in json type

if __name__ == "__main__": #is used to execute some code only if the file was run directly, and not imported.
    app.run(debug=True)
