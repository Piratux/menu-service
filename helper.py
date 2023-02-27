import datetime

import pandas as pd

def error_query(error_msg = ''):
    return pd.DataFrame({"result": "ERROR: " + error_msg}, index=[0]).to_json()

def ok_query():
    return pd.DataFrame({"result": "OK"}, index=[0]).to_json()


def is_valid_date(date_text):
    try:
        date = datetime.datetime.strptime(date_text, '%Y-%m-%d')
        if date.date() > datetime.datetime.now().date():
            print("ERROR - date '" + date_text + "' is invalid (should be less than today's date)!")
            return False

        return True
    except ValueError:
        print("ERROR - date '" + date_text + "' is invalid (should be YYYY-MM-DD)!")
        return False
