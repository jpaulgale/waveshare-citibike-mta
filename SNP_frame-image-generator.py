from PIL import Image, ImageDraw, ImageFont
import datetime
import json
import time
import os
import glob
import asyncio
from SNPCitibikeChecker import update_stations
from SNPfTrainChecker import create_arrival_json
from telegram_notifier import send_telegram_message

start_time = time.time()


def load_json(file_path):
    with open(file_path) as f:
        return json.load(f)


def draw_text(draw, x, y, text, font, fill="black"):
    draw.text((x, y), text, font=font, fill=fill)


def delete_old_frames(directory, keep=5):
    # Find all PNG files in the directory ending with "_snp-frame.png"
    files = glob.glob(os.path.join(directory, "*_snp-frame.png"))

    # Sort files by creation time (newest first)
    files.sort(key=os.path.getctime, reverse=True)

    # Delete all but the 5 newest files
    for file in files[keep:]:
        os.remove(file)


# Load template image
try:
    template = Image.open("source_files/template_snp-frame.png")
except FileNotFoundError as e:
    asyncio.run(send_telegram_message(f"File not found: template_snp-frame.png"))
except Exception as e:
    asyncio.run(send_telegram_message(f"Failed to load template_snp-frame.png: {e}"))

update_stations()
try:
    with open("latestJSONs/stations.json") as f:
        stations = json.load(f)
except FileNotFoundError as e:
    asyncio.run(send_telegram_message(f"File not found: stations.json"))
except Exception as e:
    asyncio.run(send_telegram_message(f"Failed to load stations.json: {e}"))


create_arrival_json()
try:
    with open("latestJSONs/arrival_times.json") as f:
        FTrainArrivalTimes = json.load(f)
except FileNotFoundError as e:
    asyncio.run(send_telegram_message(f"File not found: arrival_times.json"))
except Exception as e:
    asyncio.run(send_telegram_message(f"Failed to load arrival_times.json: {e}"))

uptown_times = FTrainArrivalTimes["uptown"]
downtown_times = FTrainArrivalTimes["downtown"]

# Add dynamic text
draw = ImageDraw.Draw(template)
subwayFont = ImageFont.truetype("source_files/Arial.ttf", 24)
citibikeFont = ImageFont.truetype("source_files/Arial.ttf", 28)
smallFont = ImageFont.truetype("source_files/Arial.ttf", 16)
positions = {
    "c38e2cfc-04e6-419c-8bf8-d8713ccf6ea7": {"x": 240, "y": 310},
    "c71cca54-17f6-42bc-ba94-3f5bd9c70197": {"x": 470, "y": 310},
}

for station in stations:
    x = positions[station["id"]]["x"]
    y = positions[station["id"]]["y"]

    draw_text(draw, x, y, f"{station['ebikes']}", citibikeFont)
    draw_text(draw, x + 70, y, f"{station['classic']}", citibikeFont)

for i, arrival in enumerate(uptown_times):
    draw_text(draw, 350 + i * 80, 62, arrival, subwayFont)

for i, arrival in enumerate(downtown_times):
    draw_text(draw, 350 + i * 80, 139, arrival, subwayFont)

# Get current time
now = datetime.datetime.now()

# Format it as MM/DD HH:mm:ss p
formatted_now = now.strftime("%I:%M:%S %p %m/%d")
draw_text(draw, 145, 435, f"{formatted_now}", smallFont)

# Save with timestamp
time_str = time.strftime("%Y-%m-%d_%I%M%p")
output_file = f"latest_images/{time_str}_snp-frame.png"

template.save(output_file)

delete_old_frames("latest_images")

print(f"Saved frame to {output_file}")
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Execution time: {elapsed_time:.4f} seconds")
