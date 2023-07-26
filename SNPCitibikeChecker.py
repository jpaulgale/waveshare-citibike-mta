import requests
import time
import json

start_time = time.time()

def update_stations():
    # Station IDs and names
    all_stations = []
    station_ids = ['c71cca54-17f6-42bc-ba94-3f5bd9c70197', 'c38e2cfc-04e6-419c-8bf8-d8713ccf6ea7']
    station_names = ['Bridge St & Water St', 'Bridge St & York St']

    station_status_url = 'https://gbfs.citibikenyc.com/gbfs/en/station_status.json?fields=station_id,num_bikes_available,num_ebikes_available'

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(station_status_url, headers=headers)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        station_status = response.json()

        for i in range(len(station_ids)):
            station_id = station_ids[i]
            station_name = station_names[i]

            # Find station data
            station_data = None
            for station in station_status['data']['stations']:
                if station['station_id'] == station_id:
                    station_data = station
                    break

            if station_data is None:
                print(f"Station {station_id} not found")
                continue

            ebike_count = station_data['num_ebikes_available']
            classicbike_count = station_data['num_bikes_available']

            station = {
                "id": station_id,
                "name": station_name,
                "classic": classicbike_count,
                "ebikes": ebike_count
            }

            all_stations.append(station)

        with open('/home/pi/SNP_frame-image-generator/latestJSONs/stations.json', 'w') as f:
            json.dump(all_stations, f)

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        error_data = []
        for i in range(len(station_ids)):
            station_id = station_ids[i]
            station_name = station_names[i]
            error_station = {
                "id": station_id,
                "name": station_name,
                "classic": "N/A",
                "ebikes": "N/A"
            }
            error_data.append(error_station)
            
        with open('/home/pi/SNP_frame-image-generator/latestJSONs/stations.json', 'w') as f:
            json.dump(error_data, f)

update_stations()