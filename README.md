# Assignment

Working FastAPI fetch Latest news from google news/twitters also adding sentimental score

# How to Run

hypercorn myapis:app --reload

# How to Use
Run http://127.0.0.1:8000/news?search=ENTER_QUERY_HERE

Example: 
1. http://127.0.0.1:8000/news?search=Green%20Hydrogen
2. http://127.0.0.1:8000/news?search=Modi

# API Response

Reponse will the .csv file containing 5 columnns
1. Date of news/twitter
2. Tweet content/news headline
3. Source of news / person name
4. Sentiment Prediction Label
5. Sentiment Prediction Score
