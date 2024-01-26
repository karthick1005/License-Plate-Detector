import json

import requests
import datetime

def upload_file_to_firebase(file_path, storage_path, firebase_api_key):
    url = f'https://firebasestorage.googleapis.com/v0/b/{your_project_id}.appspot.com/o/{storage_path}'
    params = {'key': firebase_api_key}

    with open(file_path, 'rb') as file:
        file_content = file.read()

    headers = {'Content-Type': 'application/octet-stream'}

    response = requests.post(url, params=params, headers=headers, data=file_content)
    print(url)
    if response.status_code == 200:
        print(f"File {file_path} uploaded to {storage_path}")
    else:
        print(f"Error uploading file: {response.text}")
    print(response.json().get('downloadTokens'))
    image_url = f"https://firebasestorage.googleapis.com/v0/b/testing-b3628.appspot.com/o/{storage_path}?alt=media&token={response.json().get('downloadTokens')}"
    print(image_url)
    return image_url


your_project_id = 'testing-b3628'
your_firebase_api_key = 'AIzaSyCWjzXRA7pNclWTsl2a-EFnpg2En_cCbQ8'


def uploadtodatabase(carnumber,state):
    current_datetime = datetime.datetime.now().strftime("%H:%M:%S %p")
    # print(current_datetime)
    current_date = datetime.datetime.now().strftime("%Y-%m-%d_%A")
    if carnumber is None:
        firebase_database_url = f'https://testing-b3628-default-rtdb.firebaseio.com/Noliscence/{current_date}/{current_datetime}'
        url = upload_file_to_firebase('detected_vehicle.png', f'{current_datetime}', your_firebase_api_key)
    else:
        url= upload_file_to_firebase('detected_vehicle.png',f'{carnumber}',your_firebase_api_key)
        firebase_database_url = f'https://testing-b3628-default-rtdb.firebaseio.com/Liscence/{current_date}/{carnumber}'

    # Firebase REST API endpoint
    firebase_endpoint = f"{firebase_database_url}.json"

    # Sample data to be pushed to Firebase
    data_to_push = {
        'Platenumber': carnumber,
        'state':state,
        'image':url,
        'Time':current_datetime
    }

    print(firebase_endpoint)

    # Send a POST request to push data to Firebase
    response = requests.put(
        firebase_endpoint,
        params={'auth': your_firebase_api_key},  # Use the private key from the service account
        json=data_to_push
    )

    # Check the response
    if response.ok:
        print("Data pushed successfully!")
    else:
        print(f"Error: {response.status_code} - {response.text}")

