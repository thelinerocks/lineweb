
# Replace or verify the region.
#
# You must use the same region in your REST API call as you used to obtain your access keys.
# For example, if you obtained your access keys from the westus region, replace
# "westcentralus" in the URI below with "westus".
#
# NOTE: Free trial access keys are generated in the westcentralus region, so if you are using
# a free trial access key, you should not need to change this region.
uri = 'westus.api.cognitive.microsoft.com'
path = '/text/analytics/v2.0/sentiment'


import http.client, urllib.request, urllib.parse, urllib.error, base64, sys, json
import requests
import numpy as np


def get_text_sentiment(documents):
    headers = {
        # Request headers. Replace the placeholder key below with your subscription key.
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'bfe8d2f23e1c40818461bc5b07f4207f',
    }

    params = urllib.parse.urlencode({
    })

    # Replace the example URL below with the URL of the image you want to analyze.
    try:
        response = requests.post("https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment", headers=headers, params={}, json=documents)
        data = response.json()
        return data
    except Exception as e:
        print(e.args)
