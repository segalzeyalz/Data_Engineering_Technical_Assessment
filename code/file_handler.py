import json
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from datetime import datetime
from db_config import ObjectsDetection, VehiclesStatus

class FileHandler(FileSystemEventHandler):
    def __init__(self, session):
        self.session = session

    def on_created(self, event: FileSystemEvent):
        if not event.is_directory:
            if "objects_detection" in event.src_path:
                self.process_objects_detection(event.src_path)
            elif "vehicles_status" in event.src_path:
                self.process_vehicles_status(event.src_path)

    def process_objects_detection(self, file_path: str):
        with open(file_path, 'r') as file:
            data = json.load(file)
            for event in data['objects_detection_events']:
                for detection in event['detections']:
                    new_record = ObjectsDetection(
                        vehicle_id=event['vehicle_id'],
                        detection_time=datetime.fromisoformat(event['detection_time']),
                        object_type=detection['object_type'],
                        object_value=detection['object_value']
                    )
                    self.session.add(new_record)
            self.session.commit()

    def process_vehicles_status(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            for status in data['vehicle_status']:
                new_status = VehiclesStatus(
                    vehicle_id=status['vehicle_id'],
                    report_time=datetime.fromisoformat(status['report_time']),
                    status=status['status']
                )
                self.session.add(new_status)
            self.session.commit()
