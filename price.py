import requests
import json
import pandas as pd
import time

def get_daily_statistics(): # get this to catch http as well or pass to another kraken function if fail
    """
    btc daily high, low and average from current time,
    data from coincap
    """
    # get prices
    # coincap max: 200 requests per minute
    url = "http://api.coincap.io/v2/assets/bitcoin/history?interval=m1"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers = headers, data = payload)

    # store data
    json_data = json.loads(response.text.encode("utf8"))
    bitcoin_data = json_data["data"]    # stuff we need but still in json
    df = pd.DataFrame(bitcoin_data, columns = ["time", "priceUsd"]) # turn json to dataframe
    df["priceUsd"] = pd.to_numeric(df["priceUsd"], errors = "coerce").fillna(0, downcast = "infer")

    # statistics
    high = round(df["priceUsd"].max())
    low = round(df["priceUsd"].min())
    average = round(df["priceUsd"].mean())
    return high, low, average

# debug
""" high, low, average = get_daily_statistics()
print(f"High: {high}")
print(f"Low: {low}")
print(f"Average: {average}") """


def new_get_price():
    url = "http://api.coincap.io/v2/assets/bitcoin"
    payload = {}
    headers = {"User-Agent" : "Mozilla/5.0"}

    # get around errors in website
    try:
        response = requests.request("GET", url, headers = headers, data = payload)
        json_data = json.loads(response.text.encode("utf8"))

        # store data
        current_time = int(json_data["timestamp"])
        current_price = float(json_data["data"]["priceUsd"])

    except requests.ConnectionError:
        return -1, None, None
    
    except json.decoder.JSONDecodeError:
        return -2, None, None
    
    if response.status_code != 200:
        return response.status_code, None, None
    
    # otherwise
    return response.status_code, current_time, current_price

def update():
    code, t, p = new_get_price()
    if code != 200:
        time.sleep(2)
        code, t, p = new_get_price()
    else:
        return t, p