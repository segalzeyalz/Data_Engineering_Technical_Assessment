import time
import logging
from watchdog.observers import Observer
from db_config import configure_db
from file_handler import FileHandler

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    logging.info("Starting the application.")
    session = configure_db()
    logging.info("Database configured successfully.")

    event_handler = FileHandler(session)
    observer = Observer()
    observer.schedule(event_handler, path='data', recursive=False)
    logging.info("File observer scheduled to watch the 'data' directory.")

    observer.start()
    logging.info("File observer started.")
    try:
        while True:
            logging.info("Application running. Waiting for file events...")
            time.sleep(10)
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt received. Stopping observer...")
        observer.stop()
    observer.join()
    logging.info("Observer stopped.")

if __name__ == '__main__':
    main()
