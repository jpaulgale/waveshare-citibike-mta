import requests
import time
import json
import asyncio
from telegram_notifier import send_telegram_message

start_time = time.time()


def update_stations():
    # Station IDs and names
    all_stations = []
    station_ids = [
        "c71cca54-17f6-42bc-ba94-3f5bd9c70197",
        "c38e2cfc-04e6-419c-8bf8-d8713ccf6ea7",
    ]
    station_names = [
        "Bridge St & Front St",
        "Bridge St & York St",
    ]

    station_status_url = "https://gbfs.lyft.com/gbfs/2.3/bkn/en/station_status.json"

    try:
        headers = {"User-Agent": "waveshare-citibike-mta/1.0"}
        response = requests.get(station_status_url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        station_status = response.json()

        for i in range(len(station_ids)):
            station_id = station_ids[i]
            station_name = station_names[i]

            # Find station data
            station_data = None
            for station in station_status["data"]["stations"]:
                if station["station_id"] == station_id:
                    station_data = station
                    break

            if station_data is None:
                print(f"Station {station_id} not found")
                continue

            # Parse vehicle types to get accurate counts
            # And set both to N/A as default in case gbfs structure changes in future
            classicbike_count = "N/A"
            ebike_count = "N/A"

            if "vehicle_types_available" in station_data:
                for vehicle_type in station_data["vehicle_types_available"]:
                    if vehicle_type["vehicle_type_id"] == "1":  # Classic bikes
                        classicbike_count = vehicle_type["count"]
                    elif vehicle_type["vehicle_type_id"] == "2":  # E-bikes
                        ebike_count = vehicle_type["count"]

            station = {
                "id": station_id,
                "name": station_name,
                "classic": classicbike_count,
                "ebikes": ebike_count,
            }

            all_stations.append(station)

        try:
            with open("latestJSONs/stations.json", "w") as f:
                json.dump(all_stations, f)
        except FileNotFoundError as e:
            asyncio.run(send_telegram_message(f"File not found: stations.json"))
        except Exception as e:
            asyncio.run(send_telegram_message(f"Failed to write to stations.json: {e}"))

    except Exception as e:
        error_message = f"Error occurred: {str(e)}"
        print(error_message)
        asyncio.run(send_telegram_message(error_message))
        error_data = []
        for i in range(len(station_ids)):
            station_id = station_ids[i]
            station_name = station_names[i]
            error_station = {
                "id": station_id,
                "name": station_name,
                "classic": "N/A",
                "ebikes": "N/A",
            }
            error_data.append(error_station)

        with open("latestJSONs/stations.json", "w") as f:
            json.dump(error_data, f)
