import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", passwd="rootpw", database="testdb")
mycursor = mydb.cursor()


def get_list_of_ids():
    # iterates through the selected list and adds result to list.
    list_of_driver_ids = []
    mycursor.execute("SELECT driver_id FROM driver")
    for x in mycursor:
        list_of_driver_ids.append(x[0])  # x[0] because cursor gives back type tuple
    return list_of_driver_ids


def build_exec_string(customer_id, year, quarter):
    #  builds string for SQL query
    exec_string = "SELECT session_id FROM results WHERE driver_id =" + str(customer_id) + \
                  " AND event_year =" + str(year) + " AND event_quarter =" + str(quarter)
    return exec_string


def insert_race_result(customer_id, input_dict):
    # inserts result in database
    session_id = str(input_dict['session_id'])
    driver_id = str(customer_id)
    start_time = str(input_dict['start_time']).replace("T", " ").replace("Z", "")
    car_name = str(input_dict['car_name'])
    series_name = str(input_dict['series_name'])
    track_name = str(input_dict['track']['track_name'])
    starting_position = str(input_dict['starting_position_in_class'])
    finishing_position = str(input_dict['finish_position_in_class'])
    incidents = str(input_dict['incidents'])
    sof = str(input_dict['event_strength_of_field'])
    championship_points = str(input_dict['champ_points'])
    event_year = str(input_dict['season_year'])
    event_quarter = str(input_dict['season_quarter'])

    sql = "INSERT INTO results VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (session_id, driver_id, start_time, car_name, series_name, track_name, starting_position, finishing_position, incidents, sof, championship_points, event_year, event_quarter)
    mycursor.execute(sql, val)
    mydb.commit()


def insert_car_data(car_dict, discipline):
    car_id = str(car_dict["car_id"])
    car_name = str(car_dict["car_name"])
    sql = "INSERT IGNORE INTO cars (car_id, car_name, discipline) VALUES (%s,%s,%s)"
    val = (car_id, car_name, discipline,)
    mycursor.execute(sql, val)
    mydb.commit()


def count_races(customer_id, year, quarter):
    # returns count of races in database with given parameters
    list_of_events = []
    mycursor.execute(build_exec_string(customer_id, year, quarter))
    for x in mycursor:
        list_of_events.append(x[0])
    return len(list_of_events)
