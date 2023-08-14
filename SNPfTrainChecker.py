import datetime
from nyct_gtfs import NYCTFeed
import json
from telegram import Bot

def send_telegram_message(message):
    bot_token = '6526779341:AAH18zjhXOWELppO8G99DVmeDQDpt8t1d3Y'
    chat_id = '6439202731'
    bot = Bot(token=bot_token)
    bot.send_message(chat_id=chat_id, text=message)

def get_next_arrivals(feed, stop_id):
    trains = feed.trips
    arrivals = []

    for train in trains:
        for stop_time_update in train.stop_time_updates:
            if stop_time_update.stop_id == stop_id:
                arrivals.append(stop_time_update.arrival)
    
    arrivals.sort()
    return arrivals[:5]

def format_arrival_times(arrivals):
    now = datetime.datetime.now()
    formatted_times = []

    for arrival in arrivals:
        minutes_until_arrival = int((arrival - now).total_seconds() // 60)

        # Ignore arrival times before now and up to 5 minutes from now negative time differences
        if minutes_until_arrival <= 5:
            continue

        formatted_time = arrival.strftime("%I:%M")
        formatted_times.append(f"{formatted_time}")

        # Stop adding times once we have 3
        if len(formatted_times) == 3:
            break
    return formatted_times

def create_arrival_json():
    try:
        api_key = "0xQojNG2st3aLmcj3phx1RYWk4TO6ml5NIfALyVf"
        feed_F = NYCTFeed("F", api_key=api_key)

        uptownF = "F18N"
        downtownF = "F18S"

        uptown_F_arrivals = get_next_arrivals(feed_F, uptownF)
        downtown_F_arrivals = get_next_arrivals(feed_F, downtownF)

        uptown_times = format_arrival_times(uptown_F_arrivals)
        downtown_times = format_arrival_times(downtown_F_arrivals)

        # Write the times to a JSON file
        with open('/home/pi/SNP_frame-image-generator/latestJSONs/arrival_times.json', 'w') as f:
            json.dump({'uptown': uptown_times[:3] + [""] * (3 - len(uptown_times)), 'downtown': downtown_times[:3] + [""] * (3 - len(downtown_times))}, f)
    except FileNotFoundError as e:
        error_message = f"File not found: {str(e)}"
        print(error_message)
        send_telegram_message(error_message)
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        send_telegram_message(error_message)
        # Return default values in case of error
        with open('/home/pi/SNP_frame-image-generator/latestJSONs/arrival_times.json', 'w') as f:
            json.dump({'uptown': ["N/A", "", ""], 'downtown': ["N/A", "", ""]}, f)