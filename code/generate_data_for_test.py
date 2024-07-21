import os
import json
import time
from datetime import datetime, timedelta

# Ensure the data directory exists
data_dir = "data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

def generate_objects_detection_events():
    events = [
        {
            "vehicle_id": "ebab5f787798416fb2b8afc1340d7a4e",
            "detection_time": (datetime.utcnow() - timedelta(minutes=10)).isoformat(),
            "detections": [
                {"object_type": "pedestrians", "object_value": 3},
                {"object_type": "cars", "object_value": 2},
                {"object_type": "signs", "object_value": 3},
            ],
        },
        {
            "vehicle_id": "ebab5f787798416fb2b8afc1340d7a4e",
            "detection_time": (datetime.utcnow() - timedelta(minutes=5)).isoformat(),
            "detections": [
                {"object_type": "cars", "object_value": 4},
            ],
        },
        {
            "vehicle_id": "ebab5f787798416fb2b8afc1340d7a4e",
            "detection_time": datetime.utcnow().isoformat(),
            "detections": [
                {"object_type": "trucks", "object_value": 5},
                {"object_type": "obstacles", "object_value": 2},
            ],
        }
    ]
    filename = os.path.join(data_dir, f"objects_detection_{int(time.time())}.json")
    with open(filename, 'w') as file:
        json.dump({"objects_detection_events": events}, file, indent=4)

def generate_vehicle_status():
    statuses = [
        {
            "vehicle_id": "ebab5f787798416fb2b8afc1340d7a4e",
            "report_time": (datetime.utcnow() - timedelta(hours=2)).isoformat(),
            "status": "driving",
        },
        {
            "vehicle_id": "ebae3f787798416fb2b8afc1340d7a6d",
            "report_time": (datetime.utcnow() - timedelta(hours=1)).isoformat(),
            "status": "accident",
        },
        {
            "vehicle_id": "qbae3f787798416fb2b8afc1340ddf19",
            "report_time": datetime.utcnow().isoformat(),
            "status": "parking",
        }
    ]
    filename = os.path.join(data_dir, f"vehicles_status_{int(time.time())}.json")
    with open(filename, 'w') as file:
        json.dump({"vehicle_status": statuses}, file, indent=4)

def main():
    while True:
        generate_objects_detection_events()
        generate_vehicle_status()
        time.sleep(10)

if __name__ == "__main__":
    main()
