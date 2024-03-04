import requests
import os
from dotenv import load_dotenv

from db_entries import get_name_from_id
from get_license_class import get_license_class
from get_subsession_data import get_subsession_data

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")  # ID of channel chosen for bot messages
API_ENDPOINT = f"https://discord.com/api/v9/channels/{CHANNEL_ID}/messages"


def send_discord_message(customer_id, result_dict, session):

    sub_sess_data = get_subsession_data(customer_id, result_dict["subsession_id"], session)
    old_ir = sub_sess_data['oldi_rating']
    new_ir = sub_sess_data['newi_rating']
    car_number = sub_sess_data['livery']['car_number']
    name = get_name_from_id(customer_id)
    pos = result_dict["finish_position_in_class"] + 1
    track = result_dict["track"]["track_name"]
    series = result_dict["series_name"]
    starting_pos = result_dict["starting_position_in_class"] + 1
    incidents = result_dict["incidents"]

    graph = ":chart_with_upwards_trend:"
    sign = "+"
    if old_ir > new_ir:
        graph = ":chart_with_downwards_trend:"
        sign = ""
    # used to change emoji depending on iRating gain or loss

    old_sr_class = get_license_class(int(sub_sess_data["old_license_level"]))
    new_sr_class = get_license_class(int(sub_sess_data["new_license_level"]))
    old_sr = float(sub_sess_data["old_sub_level"])/100
    new_sr = float(sub_sess_data["new_sub_level"]) / 100

    message = (f":checkered_flag: New race result in :trophy: **{series}**:\n"
               f":bust_in_silhouette: **#{car_number} {name}** finished **P{pos}** at :motorway: **{track}**\n"
               f"          :stopwatch: Starting position: {starting_pos}\n"
               f"          :checkered_flag: Finishing position: {pos}\n"
               f"          {graph} New iRating: {new_ir} ({sign}{new_ir - old_ir})\n"
               f"          :warning: Incidents: {incidents} ({old_sr_class}{old_sr} -> {new_sr_class}{new_sr})")

    headers = {
        "Authorization": f"Bot {TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "content": message
    }

    response = requests.post(API_ENDPOINT, json=data, headers=headers)

    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message: {response.text}")
