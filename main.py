import os
import uvicorn
from fastapi import FastAPI, HTTPException, Query
from dotenv import load_dotenv
import requests

#load environment values
load_dotenv()

basic_url = os.getenv("basic_url")
if not basic_url:
    raise ValueError("API request url is not found")

app = FastAPI(
    title="driver loading ditat verification",
    description="this API will retrieve the substatus of driver on now",
    version="1.0.0",
)

@app.get("/test")
async def test():
    return {
        "result": "okay"
    }

@app.get("/get_drivers_substatus")
async def get_drivers_substatus(
    driver_id: str = Query(..., description="this is driver's unique ID"),
    ditat_token: str = Query(..., description="this is current login token of ditat")
):
    headers = {
        "Authorization": f"Ditat-Token {ditat_token}"
    }
    body= {
        "Filter": {
            "showFilterPanel": "true",
            "truckCustomGroupKeys": [],
            "driverCustomGroupKeys": [],
            "customerCustomGroupKeys": [],
            "pickupZoneKeys": [],
            "deliveryZoneKeys": [],
            "currentLegZoneKeys": [],
            "truckSideBrokerage": 0,
            "hazmat": 0,
            "status": 0,
            "hasAgentAssignment": 0,
            "fromPickupDate": 9,
            "toPickupDate": 10,
            "fromDeliveryDate": 10,
            "toDeliveryDate": 10,
            "fromCurrentLegDate": 10,
            "toCurrentLegDate": 10
        },
    "UpdateCounter": 0
    }

    respond = requests.post(url=basic_url, headers=headers, json=body)
    data = respond.json()
    trip_data = data["data"]
    if trip_data:
        all_member_trip_data = trip_data["trips"]
        if all_member_trip_data:

            for each_driver_data in all_member_trip_data:
                each_driver_trip_current_situation = each_driver_data["primaryDriverId"];
                if driver_id in each_driver_trip_current_situation:
                    return {
                        "current_status": each_driver_data["subStatus"]
                    }
            
            return {
                "current_status": "not found"
            }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, proxy_headers=True,)
