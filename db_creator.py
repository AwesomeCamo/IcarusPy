import mysql.connector
import os
from dotenv import load_dotenv

# program creates the necessary database to run other programs
# inserts all driver data into driver table

load_dotenv()
db_password = os.getenv("DATABASE_PASSWORD")
# change password in .env and user below if not using root

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=db_password
)

mycursor = mydb.cursor()

driver_ids = [330338, 378562, 504264, 676987, 744074, 751706, 804603]
first_names = ["Marco", "Inus", "Oskar", "Jozua", "Renato", "Thiago", "Ryan"]
last_names = ["Schmitz", "Bothma", "Geijersson", "Eijgenraam", "Coicev", "Oliveira", "Baker"]
discord_ids = [256511746649358337, 206519049126019072, 515238915406430218, 269805916973563904, 458087378318393366, 646440794668138527, 535873278229610513]


def create_database():
    mycursor.execute("CREATE DATABASE icarus")
    mydb.database = "icarus"
    mycursor.execute("CREATE TABLE driver (driver_id BIGINT PRIMARY KEY, first_name VARCHAR(50), last_name VARCHAR(50), discord_id BIGINT)")
    mycursor.execute(("CREATE TABLE results (session_id BIGINT, driver_id BIGINT, start_time datetime, car_name VARCHAR(50), series_name VARCHAR(100), track_name VARCHAR(100), starting_position BIGINT, finishing_position BIGINT, incidents INT, sof INT, championship_points INT, event_year INT, event_quarter INT)"))
    mycursor.execute("ALTER TABLE results ADD PRIMARY KEY(session_id, driver_id)")


def add_drivers_to_db():
    for i in range(len(driver_ids)):
        mycursor.execute("INSERT INTO driver (driver_id, first_name, last_name, discord_id) VALUES (%s,%s,%s,%s)", (driver_ids[i], first_names[i], last_names[i], discord_ids[i]))


create_database()
add_drivers_to_db()
mydb.commit()

