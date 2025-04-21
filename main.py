from pydexcom import Dexcom
from libre_link_up import LibreLinkUpClient
import json

with open("configs/credentials.json",'r') as fd:
     credentials_items = json.load(fd)
     print(credentials_items)

dexcom_users=[]
libre_users=[]
for credentials in credentials_items:
    print(credentials)
    if(credentials['type']=="Dexcom"):
        dexcom_users.append(Dexcom(
            username=credentials['username'], 
            password=credentials['password'], 
            region=credentials['region']))
    elif(credentials['type'] == "LibreLinkUp"):
        libre_users.append(LibreLinkUpClient(
        username=credentials['username'],
        password=credentials['password'],
        url=credentials['url'],
        version="4.14.0",
        ))
    else:
        print(f"Wrong type %s"%(credentials["type"]))

glucose_reading = dexcom_users[0].get_latest_glucose_reading()
print(glucose_reading)

for client in libre_users:
    client.login()

glucose_data = libre_users[0].get_raw_connection()
print(glucose_data['glucoseMeasurement']['Value'])