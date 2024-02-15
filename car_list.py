import json

from db_entries import insert_car_data


def update_car_list(session):
    # goes through iRacing API and gets list of cars, then calls insert_car_data to add new cars to database
    search_url = "https://members-ng.iracing.com/data/car/get"
    car_url = json.loads(session.get(url=search_url).text)["link"]
    list_of_car_dicts = json.loads(session.get(url=car_url).text)
    # print(list_of_car_dicts)
    for car_dict in list_of_car_dicts:
        car_info = car_dict["search_filters"]
        if "dirt" not in car_info and "oval" not in car_info or \
                "road" in car_info and "dirtroad" not in car_info:
            if "[Legacy]" not in car_dict["car_name"]:
                if "openwheel" not in car_info:
                    discipline = "Sportscar"
                else:
                    discipline = "Formula"
                insert_car_data(car_dict, discipline)

    print("Car list update complete")
