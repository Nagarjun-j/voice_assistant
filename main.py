# main.py
from fastapi import FastAPI
# from flask import Flask
import requests
# from mangum import Mangum
from datetime import datetime
import time
app = FastAPI()
# handler=Mangum(app)
###################################################################
## CORE CODE
import os
import json
import boto3 

aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')

aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

aws_session_token = os.environ.get('AWS_SESSION_TOKEN')



bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name="ap-south-1",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)
# with open('vehicle_user_report_data.json', 'r') as openfile:
#     json_object = json.load(openfile)

# with open('harrier-bsvi-festive-edition-03 copy.txt', 'r') as file:
#     data_vehicle_manual= file.read()
data_vehicle_manual="""
Pre Driving Checks Make sure that  Windshield, windows, mirrors, lights, and reflectors are clean and unobstructed.  Tools kit, jack & handle, warning triangle, owner’s manual, first aid kit and vehicle documents are available and stored at their locations. WARNING Never put any mat on top of the floor carpet near pedal region.  All doors, engine bonnet and tail gate are securely closed and latched.  All passengers are properly restrained. All occupants travelling should always wear seat belts or suitable CRS as applicable.  Objects/luggage are secure properly against slipping or tipping.   Rear seat is securely latched.  Sufficient fuel for the trip. Daily check  Tyres for abnormal wear, cracks or damage and embedded foreign material such as nails, stones, etc.   Traces of fluid and oil below vehicle. NOTE Water dripping from the air conditioning system after use is normal.  All lamps, wipers, wiper blades and horn for proper operation.  All switches, gauges and tell tales are working properly. Adjust  Seats, head restraints (if equipped) and steering wheel position.  All the mirrors properly adjusted. Weekly check  Engine oil level  Coolant level  Brake fluid level  Windshield washer fluid level  Battery electrolyte level  Fuel level NOTE  Tyre pressure to be measured at cold condition.  Check tyre pressure and condition after every 15 days including spare wheel. 
Drive Mode (If applicable)  ‘ECO ‘, ‘CITY’ and ‘SPORT’ drive modes are provided. These modes can be used to adjust engine characteristics and vehicle performance in line with desired requirement. Drive mode selection switches are provided on center console for activation.   Drive Mode Performance CITY    Increased engine Torque and Power output for BALANCED performance. It is default mode. ECO  Optimum engine Torque and Power output for FUEL EFFICIENT performance. SPORT  Produce more torque from engine.  NOTE When vehicle is in ECO or SPORT mode, by pressing current mode switch again, mode will switch to CITY mode. 
Technical Specifications Parameter Specifications Engine Model/type Capacity 2.0L KryoTec 140 PS 1956 cc Max. Engine output Max. Torque Clutch 103 kW (140 PS) at 3750 rpm 350 Nm at 1750-2500 rpm Type Outside diameter of clutch Transaxle Dry, Single Plate diaphragm type 240 mm  Model Type C635 Manual, 6-speed, Synchromesh No. Of gears 6 Forward, 1 Reverse Steering Type Power assisted-Hydraulic with Tilt & Telescopic mechanism and collapse feature Brakes Brakes Parking Brakes Front (Disc); Rear (Drum) Cable Operated mechanical 191 TECHNICAL INFORMATION Parameter Specifications Suspension Type Front: Independent lower wishbone MacPherson strut with coil spring Rear: Semi-independent Twist blade suspension with Panhard rod & coil spring   Shock absorber Front: MacPherson strut Damper twin tube with gas filled Rear: Damper twin tube with gas filled Wheels & tyres Tyres For Front & Rear, Option 1 : 235 / 70 R16 106S (Radial-Tubeless) Option 2: 235 / 65 R17 104H (Radial-Tubeless) For Spare wheel, (16 Inch) : 235/70 R16 106S (Radial, Tubeless)  Wheel rims Option 1: 6.5J X 16 steel wheel Option 2 : 7.5J X 17 alloy wheel Fuel tank Capacity 50 liters Cab / body Type Monocoque  192 TECHNICAL INFORMATION Parameter Specifications Electrical system System voltage Alternator capacity 12 Volts 110 Amp Battery 12V, 74 Ah Main chassis dimension (in mm) Wheel base Track front 2741 1616 Track rear Overall length 1630 4598 Overall height Max. Width 1706 1894 over body Ground clearance 176 mm (Laden)
"""
 
# address = '--address -- pune'

def chatmodel(prompt):
    kwargs = {
    "modelId": "anthropic.claude-3-sonnet-20240229-v1:0",
    "contentType": "application/json",
    "accept": "application/json",
    "body": json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4096,
        "messages": [
        {
            "role": "user",
            "content": [
            {
                "type": "text",
                "text": prompt
            }
                ]
            }
            ]
        })
        }
    response = bedrock_runtime.invoke_model(**kwargs)
    body = json.loads(response['body'].read())
    return body['content'][0]['text']


# function to fetch realtimeData
def get_real_time_data():
        # URL of the FastAPI endpoint
    url = "https://q789819xlj.execute-api.us-west-2.amazonaws.com/dev/cvp/v1/vehicles/data/realTimeData"
    campaigns=["TML_SANDBOX_SENSORS_TS","TML_ALERTS_TS"]
    # Payload to send in the POST request
    payload = {
        "vin": "5TMLSF102JF070824",
        "interval": {
            "hour": 100
        },
        "limit": 4096,
        "pageNumber":1,
        "campaignName" : "TML_SANDBOX_SENSORS_TS"
    }
    # Headers to send with the request
    headers = {
        "x-api-key": "VsWlUhL16R4U0w4i7xJKS8cWSN2ET3Sea05TEC7f",
        "authorization": "allow",  # Example of a custom header
        "Content-Type": "application/json"  # Add any custom headers here
    }

    # Send POST request
    response = requests.post(url, json=payload, headers=headers)

        # Check if the request was successful
    if response.status_code == 200:
        # Parse and print the JSON response
        response_data = response.json()
        return response_data
    else:
        return f"Failed to fetch data. Status code: {response.status_code}"
    


def get_latest_unique_measures(data):
    # Parse the JSON data into a list of dictionaries
    parsed_data = data["Data"]

    # Convert the 'time' field to a datetime object for accurate sorting
    for item in parsed_data:
        item['time'] = datetime.strptime(item['time'], '%Y-%m-%d %H:%M:%S.%f000')

    # Sort the data by 'measureName' and 'time' in descending order
    parsed_data.sort(key=lambda x: (x['measureName'], x['time']), reverse=True)

    # Create a dictionary to store the latest unique measureName
    unique_measures = {}
    for item in parsed_data:
        measure_name = item['measureName']
        if measure_name not in unique_measures:
            unique_measures[measure_name] = item

    # Extract the latest unique measures and convert time back to string
    result = []
    for item in unique_measures.values():
        item['time'] = item['time'].strftime('%Y-%m-%d %H:%M:%S.%f000')
        result.append(item)
    if len(result)>100:
        return result[:100]
    else:
        return result
###################################################################
## ENDPOINTS

@app.get("/")
def read_root():
    return {"message": "Hello, I am Voice Assistant for HARRIER!"}

@app.get("/query_manual/{query}")
def query_manual(query: str = None):    
    prompt_vehicle_manual=f'This is question:{query}. This question should be answered from the data: {data_vehicle_manual}. This is actually a manual of TATA Motors Harrier car. Generate suitable, specific and concise answer. Limit answer length to 20 words.'
    result = chatmodel(prompt_vehicle_manual)
    return {'result': result}

@app.get("/query_real_time_data/{query}")
def query_real_time_data(query: str = None):

    # function to fetch realtimeData
    data_real_time_data=get_real_time_data()
    data_real_time_data=get_latest_unique_measures(data_real_time_data)
    prompt_real_time_data=f'This is question:{query}. This question should be answered from the DATA: {data_real_time_data}. This is actually a JSON of telemetry data of TATA Motors Harrier car. Generate suitable, specific and concise answer. Limit answer length to 20 words. if DATA is empty, say NO DATA RECEIVED FROM CAR.'
    result = chatmodel(prompt_real_time_data)
    return {'result': result}

@app.get("/check_remote_status/{query}")
def check_remote_status(query: str = None):

    # function to fetch realtimeData
    data_real_time_data=get_real_time_data()
    data_real_time_data=get_latest_unique_measures(data_real_time_data)
    prompt_real_time_data=f'This is question:{query}. This question is about remote status of vehicle. Ensure to fetch latest status value here. This question should be answered from the DATA: {data_real_time_data}. This is actually a JSON of telemetry data of TATA Motors Harrier car. Generate suitable, specific and concise answer. Limit answer length to 20 words. if DATA is empty, say NO DATA RECEIVED FROM CAR.'
    result = chatmodel(prompt_real_time_data)
    
    return {'result': result}

@app.get("/send_command/{query}")
def send_command(query: str = None):
    query=query.lower()
    ###########################
    if 'lock' in query:
        VSS_signal='Vehicle.Cabin.Door.IsLockedCommand'
        if 'unlock' in query:
            value=0
        else:
            value=1
    elif 'ac' in query:
        VSS_signal='Vehicle.Cabin.HVAC.IsAirConditioningActiveCommand'
    elif 'light' in query:
        VSS_signal='Vehicle.Body.Lights.Approch.IsOnCommand'
    elif 'horn' in query:
        VSS_signal='Vehicle.Body.Horn.IsActiveCommand'
    if 'on' in query or 'horn' in query:
        value=1
    else:
        value=0
    

    ###########################


        # URL of the FastAPI endpoint
    url = "https://q789819xlj.execute-api.us-west-2.amazonaws.com/dev/v1/vehicles/commands"
    # campaigns=["TML_SANDBOX_SENSORS_TS","TML_ALERTS_TS"]
    # Payload to send in the POST request
    payload ={
        "vin": "5TMLSF102JF070824", # VIN
        "receiver": VSS_signal, # VSS_signal
        "value": {
            "integerValue": value # value
        }
    }

    # Headers to send with the request
    headers = {
        "x-api-key": "VsWlUhL16R4U0w4i7xJKS8cWSN2ET3Sea05TEC7f",
        "authorization": "allow",  # Example of a custom header
        "Content-Type": "application/json"  # Add any custom headers here
    }

    # Send POST request
    response = requests.post(url, json=payload, headers=headers)
    time.sleep(2)
        # Check if the request was successful
    if response.status_code == 200:
        # Parse and print the JSON response
        response_data = response.json()

        # ------------------------------------------
        # check command execution status
        url = "https://q789819xlj.execute-api.us-west-2.amazonaws.com/cnc/v1/vehicles/commands/"+response_data['id']

        # Headers to send with the request
        headers = {
            "x-api-key": "gR0vowWiYo2YR5hHzyOCd6pvEwYwUIko9foRQhu2",
            "authorization": "allow",  # Example of a custom header
            "Content-Type": "application/json"  # Add any custom headers here
        }

        # Send POST request
        response_ex_status = requests.get(url, headers=headers)
        time.sleep(2)
        if response_ex_status.status_code == 200:
            # Parse and print the JSON response
            return response_ex_status #.json()
    else:
        return f"Failed..."
