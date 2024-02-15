import requests
import pickle


def iracing_auth():
    # authorizes with iRacing and stores cookie in cookie-jar.txt
    inputs = {"email": "camo2708@gmail.com", "password": "0YmkXYQRxB0R3GAOoMejV2atCSGvFXnOZLzgGzd0Frc="}
    session = requests.Session()
    session.post(url="https://members-ng.iracing.com/auth", data=inputs)
    with open('./cookie-jar.txt', 'wb') as f:
        pickle.dump(session.cookies, f)
    print("reauthorized")


def check_auth():
    # checks if existing cookie works for auth
    session = requests.Session()
    with open('./cookie-jar.txt', 'rb') as f:
        session.cookies.update(pickle.load(f))
    check_output = session.get(url="https://members-ng.iracing.com/data/member/info")  # tries to do api call
    if "error" in check_output.text:  # checks if previous api call worked, if not, call iracing_auth func
        print("Re-authorization needed")
        iracing_auth()
    else:
        print("check worked")

