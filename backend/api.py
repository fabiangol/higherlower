from fastapi import FastAPI
import random
import uvicorn
from pytrends.exceptions import ResponseError

from pytrends.request import TrendReq

timeframe_dict = {
    "all-time": ('all', ),
    "past-day": ('now 1-H', 'now 4-H'),
    "past-week": ('today 1-d', 'today 7-d'),
    "past-year": ('today 1-m', 'today 3-m', 'today 12-m'),
}
geo_tuple = ('DE', 'US', )

app = FastAPI()

@app.get("/random-number")
def get_random_number():
    return {"number": random.randint(1, 100)}

@app.get("/mock-prompt")
def get_mock_prompt():
    r = random.randint(1, 100)
    return {
        "prompt": r,
        "value": r,
    }

@app.get("/random-prompt")
def get_random_prompt():
    req = TrendReq()

    timeframe = get_random_timeframe()
    geo = get_random_geo()

    data_frame_today = req.today_searches(pn=geo)

    prompt_string = ''.join(data_frame_today[random.randint(0, len(data_frame_today)-1)])
    search_term = extract_search_term(prompt_string)

    # Interactions with timeframe based information have to be made try-catch, as g-trends gives
    # 400 for search-terms that are not frequently queried
    try:
        req.build_payload(kw_list=[search_term], cat=0, timeframe=timeframe, geo=geo, gprop='')
        data_frame_interest = req.interest_over_time()
        search_term_sum = data_frame_interest[search_term].sum()
        return {
            "search-term": search_term,
            "geo": geo,
            "timeframe": timeframe,
            "sum": int(search_term_sum)
        }
    except (ValueError, ResponseError) as e:
        print(f'Timeframe {timeframe} did not yield meaningful results for geo {geo} with search term {search_term}')
        return {
            "error": "No meaningful results",
            "search-term": search_term,
            "geo": geo,
            "timeframe": timeframe
        }


def get_random_geo():
    """Select a random geolocation from the geo tuple"""
    return random.choice(list(geo_tuple))

def get_random_timeframe():
    """Select a random timeframe from the dictionary of timeframes"""
    timeframe_category = random.choice(list(timeframe_dict.keys()))
    timeframe_opts = timeframe_dict[timeframe_category]
    return random.choice(list(timeframe_opts))

def extract_search_term(prompt_string):
    """Extract the search term from a prompt by splitting after ?q="""
    return prompt_string.split('?q=')[1].split('&')[0]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
