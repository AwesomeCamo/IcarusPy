import json
import pickle
import requests

from auth import check_auth
from car_list import update_car_list
from db_entries import get_list_of_ids, count_races, insert_race_result


def get_race_results(session, customer_id, year, quarter):
    search_url = ("https://members-ng.iracing.com/data/results/search_series?cust_id=" + customer_id +
                  "&season_year=" + year + "&event_types=5&season_quarter=" + quarter + "&official_only=true")
    response = session.get(url=search_url)
    results_dict = json.loads(response.text)
    if results_dict["data"]["chunk_info"]["chunk_file_names"] != []:
        link_to_results = results_dict["data"]["chunk_info"]["base_download_url"] + \
                          results_dict["data"]["chunk_info"]["chunk_file_names"][0]
        initial_result_list = requests.get(link_to_results).text
        result_list = initial_result_list.strip('][').split(', ')
        for i in range(count_races(customer_id, year, quarter), len(result_list)):
            # loop starts at first race result that is not in database
            current_result_dict = json.loads(result_list[i])
            insert_race_result(customer_id, current_result_dict)
            print("Race added for driver %s" % customer_id)
        # goes through all the steps of getting to a user's results and converts them
        # into a list for further usage. Results that are not in database yet are added


def main():
    check_auth()
    session = requests.Session()
    with open('./cookie-jar.txt', 'rb') as f:
        session.cookies.update(pickle.load(f))
    # update_car_list(session)
    # above func is only needed when new cars are added to iRacing
    for i in range(len(get_list_of_ids())):
        print("Querying results for driver", get_list_of_ids()[i])
        get_race_results(session, str(get_list_of_ids()[i]), str(2024), str(1))


main()

