
import pandas as pd
import requests
from fuzzywuzzy import fuzz 
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
stop=['your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 
"she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 
'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 
'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be',
'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',
'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
'while', 'of', 'at']
df['Questions_cleaned']=df['Questions'].apply(lambda x: [item for item in x.split() if item not in stop])
get_responses=df['Answers']
def joining(s):
    return ''.join(s)
df['Questions_cleaned']=df['Questions_cleaned'].apply(joining)
input_queries=df['Questions'];input_queries_cleaned=df['Questions_cleaned']

def get_best_matches(ques,a):
    return fuzz.partial_token_sort_ratio(ques,a)
def predict_best_match(input_search):
    df['Ratio']=input_queries_cleaned.apply(get_best_matches,a=input_search)
    max_threshold_value=df['Ratio'].argmax()
    threshold=df['Ratio'][max_threshold_value]
    return (True, get_responses[max_threshold_value],df['Ratio'][max_threshold_value]) if threshold > 50 else (False,input_queries[max_threshold_value],df['Ratio'][max_threshold_value])