import pickle
from flask import Flask, request,json,make_response

import numpy as np


with open('rf.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

app = Flask(__name__)

@app.route('/')

def hello():
    return 'Hey Mayank its working fine'

@app.route('/webhook',methods=['POST','GET'])


def webhook():
    req= request.get_json(silent= True, force=True)
    
    res= processRequest(req)
    
    res=json.dumps(res,indent=4)
    
    r= make_response(res)
    
    r.headers['Contetnt-Type']='application/json'
    
    return r


def processRequest(req):
    
    sessionID= req.get('responseId')
    result= req.get("queryResult")
    user_says= result.get("queryText")
    parameters= result.get("parameters")
    
    s_length = parameters.get( "SepalLength")
    s_width = parameters.get("SepalWidth")
    p_length = parameters.get("Petallength")
    p_width = parameters.get( "PetalWidth")
    
    prediction = model.predict(np.array([[s_length, s_width, p_length, p_width]]))
    if prediction==0:
        res= 'Setosa'
    elif prediction==1:
        res= 'Versicolor'
    else:
        res= 'Verginica'
        
    fulfillmentText= " Based on the above inputs the iris flower belongs to:" + res
    
    return {
            "fulfillmentText": fulfillmentText
            }


if __name__ == '__main__':
    app.run()
    

    
    
