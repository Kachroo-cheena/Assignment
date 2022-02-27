from fastapi import FastAPI
import requests
import json
import pandas as pd
from transformers import pipeline
from fastapi.responses import FileResponse

import os


# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = "AAAAAAAAAAAAAAAAAAAAAAS%2FZgEAAAAA8y0jEu%2FyIngtc3zQXrji%2BmJnV1Y%3DkzdzjDS87FI8BE2jNGmfBquo4oyApXlRQgerwdleaJXK5JeMKR"

search_url = "https://api.twitter.com/2/tweets/search/recent"

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {'query': 'Green Hydrogen','expansions':'author_id','tweet.fields': 'author_id,created_at,source','user.fields':'description'}

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

app = FastAPI()

@app.get("/cheena")
def index():
    r = requests.get("https://gnews.io/api/v4/search?q={0}&token=575c38a2882fcb51d4d9b116640e890e&from=2022-02-01T00:00:00Z".format("Green Hydrogen"))
    myjson = json.loads(r.text)
    mylist = myjson["articles"]
    title = []
    url = []
    publish = []
    label = []
    score = []
    sentiment_pipeline = pipeline("sentiment-analysis")

    for m in mylist:
        title.append(m["title"])
        url.append(m["url"])
        publish.append(m["publishedAt"])
        data = [m["title"]]
        temp = sentiment_pipeline(data)[0]
        label.append(temp['label'])
        score.append(temp["score"])
        # label.append('')
        # score.append('')

    
    json_response = connect_to_endpoint(search_url, query_params)
    tweet_data = json_response["data"]
    tweet_users = json_response["includes"]["users"]
    for d,u in zip(tweet_data,tweet_users):
        title.append(d["text"])
        url.append(u["name"])
        publish.append(d["created_at"])
        temp = sentiment_pipeline(d["text"])[0]
        label.append(temp['label'])
        score.append(temp["score"])
        
    t = {'Date of News/Tweet':publish,'Tweet content/news headline':title,'source of news / person name who has tweeted':url,"Predicted Sentimental Label":label,"Predicted Sentimental Score":score}
    df = pd.DataFrame(t)
    df.to_csv("Cheena_News.csv")
    file_path = "Cheena_News.csv"
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="text/csv", filename="Cheena_csv.csv")
    return {"error" : "File not found!"}


    # return "This is an index page"
