#!/usr/bin/env python

import urllib
import json
import os
import requests

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    #print("Request:")
    #print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def makeWebhookResult(req):

    #if req.get("result").get("action") != "light":
        #return {}
    
    result = req.get("result")
    parameters = result.get("parameters")
    state = parameters.get("light1")
    brightness = parameters.get("number")

    if state == "":
        state = 'on'
    
    if brightness == "":
        brightness = 250
    elif int(brightness) > 250:
        brightness = 250
    else:
        brightness = int(brightness)
    
    #print(json.dumps(item, indent=4))

    url = "http://ac9baf93.ngrok.io/api/PwZ5n9cSlbRssx0bMipb69lNIj4Sn7m8vTLwS2bR/lights/6/state"

    body = {"on": True,"bri": brightness}
    
    print("State:")
    print(state)
    
    print("URL:")
    print(url)
    
    print("BODY:")
    print(body)
    
    
    if state == 'on':
        body = {"on": True,"bri": brightness}
    else:
        body = {"on": False, "bri": 0 }

    response = requests.put(url, data=json.dumps(body))

    if response.status_code == 200:
        if state == 'on':
            speech = "The light is now switched " + state + " with brightness of " + str(brightness)
        if state == 'off':
            speech = "The light is now switched " + state
    else:
        speech = "The light was not switched " + state + " due to an error. Please try again."

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "ifog_light_hue"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print('Starting app on port %d' % port)

    app.run(debug=True, port=port, host='0.0.0.0')
