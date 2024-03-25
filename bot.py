import schedule
import time
import requests

# Your Discord webhook URL
WEBHOOK_URL = 'https://discord.com/api/webhooks/1221726494213279756/3dFSf14g7nS7y2hnHUBjoJxWFaHB7O4w0EVZMzPteJ5wH_Ztb0oHQzonX-m2u9-SEMc-'

# Define the message content for notifications
morning_message = "Warehouse open, start hitting those orders NOW🎯"
afternoon_message = "⏰Shipping window closing HIT NOW 1 hour left for closure⏰"
evening_message = "Window closed, packages being delivered ... "
sunday_morning_message = "Monday preload hits, start orders now for monday shipping"
sunday_evening_message = "📦START HITS NOW FOR MONDAY DISPATCH📦"

# Function to fetch current time from TimezoneDB API
def get_current_time():
    url = "http://api.timezonedb.com/v2.1/get-time-zone"
    params = {
        "key": "ZOKX49M4TIYN",  # Replace with your TimezoneDB API key
        "format": "json",
        "by": "zone",
        "zone": "Europe/London"  # UK timezone
    }
    response = requests.get(url, params=params)
    data = response.json()
    current_time = data['formatted']
    return current_time

# Function to send notification
def send_notification(message):
    data = {
        "content": message
    }
    requests.post(WEBHOOK_URL, json=data)

# Define the job scheduling
def schedule_jobs():
    while True:
        current_time = get_current_time()
        if current_time.endswith("09:00:00"):
            send_notification(morning_message)
            time.sleep(86400)  # Sleep for 24 hours
        elif current_time.endswith("15:00:00"):
            send_notification(afternoon_message)
            time.sleep(86400)  # Sleep for 24 hours
        elif current_time.endswith("17:00:00"):
            send_notification(evening_message)
            time.sleep(86400)  # Sleep for 24 hours
        elif current_time.startswith("Sun 09:00"):
            send_notification(sunday_morning_message)
            time.sleep(604800)  # Sleep for 7 days
        elif current_time.startswith("Sun 18:00"):
            send_notification(sunday_evening_message)
            time.sleep(604800)  # Sleep for 7 days
        else:
            time.sleep(60)  # Check every minute

if __name__ == "__main__":
    schedule_jobs()
