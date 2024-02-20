import json
import pickle
import time

import requests

from auth import check_auth
from car_list import update_car_list
from db_entries import get_list_of_ids, count_races, insert_race_result
from discord_message_sender import send_discord_message
from get_subsession_data import get_subsession_data
from series_list import get_series_list


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
            # dict in which data for one specific race is stored
            try:
                send_discord_message(customer_id, current_result_dict, session)
            except Exception as e:
                print(e)

            insert_race_result(customer_id, current_result_dict)
        # goes through all the steps of getting to a user's results and converts them
        # into a list for further usage. Results that are not in database yet are added


def main():
    check_auth()
    session = requests.Session()
    with open('./cookie-jar.txt', 'rb') as f:
        session.cookies.update(pickle.load(f))
    # update_car_list(session)
    # get_series_list(session)
    # above funcs are only needed when new content is added to iRacing
    for i in range(len(get_list_of_ids())):
        print("Querying results for driver", get_list_of_ids()[i])
        get_race_results(session, str(get_list_of_ids()[i]), str(2024), str(1))


while True:
    main()
    print("Check complete - sleeping for 5 minutes")
    time.sleep(300)

