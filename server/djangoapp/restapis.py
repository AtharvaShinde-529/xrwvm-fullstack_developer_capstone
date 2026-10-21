import os
import requests
import sys
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

backend_url = os.environ.get('backend_url')
sentiment_analyzer_url = os.environ.get('sentiment_analyzer_url')

def get_request(endpoint, **kwargs):
    params = ""
    if(kwargs):
        for key,value in kwargs.items():
            params=params+key+"="+value+"&"
    
    request_url = backend_url + endpoint
    if params:
        request_url = request_url + "?" + params
        
    print(f"DEBUG: GET from {request_url}", flush=True)
    try:
        response = requests.get(request_url, timeout=10)
        print(f"DEBUG: Response Status: {response.status_code}", flush=True)
        print(f"DEBUG: Response Text: {response.text[:200]}", flush=True)
        return response.json()
    except Exception as e:
        print(f"DEBUG: Network exception occurred: {e}", file=sys.stderr, flush=True)
        return []

def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url+"analyze/"+text
    try:
        response = requests.get(request_url, timeout=10)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return {}

def post_review(data_dict):
    request_url = backend_url+"/insert_review"
    try:
        response = requests.post(request_url,json=data_dict, timeout=10)
        return response.json()
    except:
        return {}
