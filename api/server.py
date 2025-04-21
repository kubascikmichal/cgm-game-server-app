from flask import Flask
from time import time
import threading

def run(users:[], ip:str="0.0.0.0", port:int=5000):
    app = Flask(__name__)
    print(users)
    actual_data = []
    last_check_time = int(time())
    for libre_user in users[1]:
        for libre_key in libre_user:
            libre_user[libre_key].login()
    @app.route("/")
    def hello_world():
        return "Hello, World!"
    
    @app.route("/getCGMData")
    def getCGMData():
        global actual_data
        return {'time':last_check_time,
                'data':actual_data}
    
    def actualize_CGM():
        print(f"new data approaching %s"%(time()))
        global actual_data, last_check_time
        last_check_time = int(time())
        actual_data = []
        for dexcom_users in users[0]:
            for account_id in dexcom_users:
                glucose_data = dexcom_users[account_id].get_current_glucose_reading()
                if glucose_data != None:
                    actual_data.append({account_id: glucose_data.mmol})
                else:
                    actual_data.append({account_id: -1})
        for libre_users in users[1]:
            for account_id in libre_users:
                glucose_data = libre_users[account_id].get_raw_connection()
                actual_data.append({account_id: glucose_data['glucoseMeasurement']['Value']})
        threading.Timer(60, actualize_CGM).start()

    actualize_CGM()
    
    app.run(ip, port)