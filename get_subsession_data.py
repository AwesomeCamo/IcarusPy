import json

# returns subsession data for accessing broader information i.e. iRating or car number
# differentiates between team race and solo race because api returns different structure


def get_subsession_data(customer_id, subsession_id, session):
    search_url = f"https://members-ng.iracing.com/data/results/get?subsession_id={subsession_id}"
    series_link = json.loads(session.get(url=search_url).text)["link"]
    subsession_data = json.loads(session.get(url=series_link).text)
    if subsession_data["max_team_drivers"] == 1:
        for driver_result in subsession_data["session_results"][2]["results"]:
            if driver_result["cust_id"] == int(customer_id):
                return driver_result
    else:
        for team_result in subsession_data["session_results"][2]["results"]:
            for driver_result in team_result["driver_results"]:
                if driver_result["cust_id"] == int(customer_id):
                    return driver_result
