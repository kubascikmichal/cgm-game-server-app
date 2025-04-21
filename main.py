from pydexcom import Dexcom
from libre_link_up import LibreLinkUpClient
import json

with open("configs/credentials.json",'r') as fd:
     credentials_items = json.load(fd)
     print(credentials_items)

dexcom_users={}
libre_users={}
for credentials in credentials_items:
    print(credentials)
    if(credentials['type']=="Dexcom"):
        dexcom_users.update({credentials['user_id'] : Dexcom(
            username=credentials['username'], 
            password=credentials['password'], 
            region=credentials['region'])})
    elif(credentials['type'] == "LibreLinkUp"):
        libre_users.update({credentials['user_id'] :LibreLinkUpClient(
        username=credentials['username'],
        password=credentials['password'],
        url=credentials['url'],
        version="4.14.0",
        )})
    else:
        print(f"Wrong type %s"%(credentials["type"]))

for dexcom_key in dexcom_users:
    print(f"id: %s, obj: %s"%(dexcom_key, dexcom_users[dexcom_key]))
    glucose_reading = dexcom_users[dexcom_key]._username
    print(glucose_reading)

for libre_key in libre_users:
    print(f"id: %s, obj: %s"%(libre_key, libre_users[libre_key]))
    libre_users[libre_key].login()
    glucose_data = libre_users[libre_key].get_raw_connection()
    print(glucose_data['glucoseMeasurement']['Value'])