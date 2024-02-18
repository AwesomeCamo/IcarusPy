import json


def get_subsession_data(customer_id, subsession_id, session):
    search_url = f"https://members-ng.iracing.com/data/results/get?subsession_id={subsession_id}"
    series_link = json.loads(session.get(url=search_url).text)["link"]
    subsession_data = json.loads(session.get(url=series_link).text)
    for driver_result in subsession_data["session_results"][2]["results"]:
        if driver_result["cust_id"] == int(customer_id):
            return driver_result
