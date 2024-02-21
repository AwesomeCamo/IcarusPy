import json

from db_entries import insert_series_data

# only used to keep track of current race series for career mode


def get_series_list(session):
    search_url = "https://members-ng.iracing.com/data/series/get"
    series_link = json.loads(session.get(url=search_url).text)["link"]
    series_list = json.loads(session.get(url=series_link).text)
    for item in series_list:
        if item["category"] == "road":
            insert_series_data(item["series_id"], item["series_name"])
