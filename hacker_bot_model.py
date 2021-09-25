
import pandas as pd
import requests
from fuzzywuzzy import fuzz ,process
global df
# from difflib import SequenceMatcher

# def similar(a, b):
#     return SequenceMatcher(None, a, b).ratio()

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
df['Questions_cleaned']=df['Questions'].apply(lambda x: [item for item in x.split(" ") if item not in stop])
get_responses=df['Answers']
def joining(s):
    return ' '.join(s)
df['Questions_cleaned']=df['Questions_cleaned'].apply(joining)
input_queries=df['Questions'];input_queries_cleaned=df['Questions_cleaned']

def get_best_matches_n(ques,a):
    return fuzz.partial_token_set_ratio(ques,a)

def get_best_matches(ques,a):
    return fuzz.partial_token_sort_ratio(ques,a)
def predict_best_match(input_search):
    global df
    mdf=df
    mdf['Ratio']=input_queries_cleaned.apply(get_best_matches,a=input_search)
    mdf=mdf.sort_values('Ratio',ascending=False)
    mdf=mdf[:10]
    mdf['Ratio']=mdf['Questions'].apply(get_best_matches_n,a=input_search)
    q_response,threshold=process.extractOne(input_search,list(mdf['Questions']))
    # print(mdf)
    # max_threshold_value=mdf['Ratio'].idxmax()
    # print(max_threshold_value)
    # threshold=mdf['Ratio'][max_threshold_value]
    # return (True, get_responses[max_threshold_value],threshold) if threshold > 50 else (False,input_queries[max_threshold_value],threshold)
    # print(mdf['Questions'])
    return (True, mdf.loc[mdf['Questions'] == q_response, 'Answers'].iloc[0],threshold) if threshold > 50 else (False,q_response,threshold)