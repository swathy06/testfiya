from flask import Flask
from flask import request
import json
import os
from flask import make_response
app = Flask(__name__)

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler('hello.log')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

logger.info('bmi')


@app.route('/',methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print("Request:")
    print(json.dumps(req, indent=4))
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):
    print("Request:")
    print(json.dumps(req, indent=4))
    if req.get("result").get("action") == "getBmi":
        data = req
        res = makeWebhookResultForGetBmi(data)
    elif req.get("result").get("action") == "getDia":
        data = req
        res = makeDia(data)
    else:
        return {}
    return res
def makeWebhookResultForGetBmi(data):
    element1 = data.get("result").get("parameters").get("number")
    print (element1)
    element2 = data.get("result").get("parameters").get("number-integer")
    element2 = int(element2)/100
    print (element2)
    bmi = float(element1)/(float(element2*element2))
    bmi =round(bmi,2)
    print(bmi)
    if (bmi<=18.5):
        a = 'underweight'
        i=float(19)*(float(element2*element2))
        print(i)
        r =  int(i) - int(element1) 
        i = round(i,2)
        speech = 'Your bmi is {} and you are {} So your ideal weight should be {}kg and you have to gain {}kg'.format(bmi, a,i,r)
    elif (bmi>18.5 and bmi<24.9):
        a = 'healthy'
        speech = 'Your bmi is {} and you are {}'.format(bmi, a)
    elif (bmi>25.0 and bmi<29.9):
        a ='overweight'
        i = float(25) * (float(element2 * element2))
        print(i)
        r = int(element1) - int(i)
        i = round(i, 2)
        speech = 'Your bmi is {} and you are {} So your ideal weight should be {}kg and you have to reduce {}kg'.format(bmi, a, i,r)
    else:
        a = 'obese'
        i = float(25) * (float(element2 * element2))
        print(i)
        r = int(element1) - int(i)
        i = round(i, 2)
        speech = 'Your bmi is {} and you are {} So your ideal weight  should be {}kg and you have to reduce {}kg'.format(bmi, a, i,r)
    #speech = 'Your bmi is {}' +str(bmi)'and you are'+str(a)
    #speech = 'Your bmi is {} and you are {}' .format(bmi,a)

    return {
        "speech": speech,
        "displayText": speech,
        "source": "webhookdata"
    }
def makeDia(data):
    element1 = data.get("result").get("parameters").get("number-integer")
    element2 = data.get("result").get("parameters").get("number")
    if (element1 < 100 and (element2 > 79 and element2 < 159)):
        a = 'normal'
       
        speech = 'Your are not diabetic'
    elif (element1 < 100 and (element2 > 160 and element2 < 200)):
        a = 'prediabetic'
        speech = 'You are {} and its better to consult a Physician. As Prevention is better than cure'.format(a)
    elif (element1 < 100 and  element2 > 200):
        a ='diabetic'
        
        speech = 'You are {} .Please consult a diabetologist and have a regular checkup'.format(a)
    else:
        a = 'diabetic'
        
        speech = 'You are {} .Please consult a diabetologist and have a regular checkup'.format(a)
    #speech = 'Your bmi is {}' +str(bmi)'and you are'+str(a)
    #speech = 'Your bmi is {} and you are {}' .format(bmi,a)

    return {
        "speech": speech,
        "displayText": speech,
        "source": "webhookdata"
    }
   

if __name__ == '__main__':
  app.run()
