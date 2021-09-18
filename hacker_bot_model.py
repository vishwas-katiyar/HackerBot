from difflib import SequenceMatcher
import pandas as pd
import requests

try:
    df=pd.read_json('indents.json')
except:
    url = 'https://github.com/vishwas-katiyar/HackerBot/raw/main/indents.json'
    r = requests.get(url, allow_redirects=True)
    with open('indents.json', 'wb') as handle:
            response = requests.get(url, stream=True)
            if not response.ok:
                print(response)
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)
    open('indents.json', 'wb').write(r.content)
df=pd.read_json('indents.json')
get_responses=df['Answers'];input_queries=df['Questions']
def get_best_matches(ques,a):
    return SequenceMatcher(None,ques,a).ratio() 
def predict_best_match(input_search):
    df['Ratio']=input_queries.apply(get_best_matches,a=input_search)
    max_threshold_value=df['Ratio'].argmax()
    threshold=df['Ratio'][max_threshold_value]
    return (True, get_responses[max_threshold_value],df['Ratio'][max_threshold_value]) if threshold > 0.5 else (False,input_queries[max_threshold_value],df['Ratio'][max_threshold_value])