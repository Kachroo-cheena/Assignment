from fastapi import FastAPI
import requests
import json
import pandas as pd
from transformers import pipeline
from fastapi.responses import FileResponse
import os
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
        label.append(sentiment_pipeline(data)[0]['label'])
        score.append(sentiment_pipeline(data)[0]['score'])
        # label.append('')
        # score.append('')

    t = {'Date of News':publish,'News Headline':title,'Source of News':url,"Predicted Sentimental Label":label,"Predicted Sentimental Score":score}
    df = pd.DataFrame(t)
    df.to_csv("Cheena_News.csv")
    file_path = "Cheena_News.csv"
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="text/csv", filename="Cheena_csv.csv")
    return {"error" : "File not found!"}


    # return "This is an index page"
