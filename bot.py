import requests
from datetime import datetime, timedelta
import time

# Your Discord webhook URL
WEBHOOK_URL = 'https://discord.com/api/webhooks/1221726494213279756/3dFSf14g7nS7y2hnHUBjoJxWFaHB7O4w0EVZMzPteJ5wH_Ztb0oHQzonX-m2u9-SEMc-'

# Define the message content for notifications
messages = {
    1: "Warehouse open, start hitting those orders NOW🎯",
    2: "⏰Shipping window closing HIT NOW 1 hour left for closure⏰",
    3: "Window closed, packages being delivered ... ",
    4: "Monday preload hits, start orders now for monday shipping",
    5: "📦START HITS NOW FOR MONDAY DISPATCH📦"
}

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
    current_time = datetime.strptime(data['formatted'], "%Y-%m-%d %H:%M:%S")
    return current_time

# Function to send notification
def send_notification(message):
    data = {
        "content": message
    }
    requests.post(WEBHOOK_URL, json=data)

# Function to display menu and handle user input
def display_menu():
    print("Choose a message to send:")
    for key, value in messages.items():
        print(f"{key}. {value}")

    while True:
        try:
            choice = int(input("Enter the number of the message you want to send (1-5): "))
            if choice in messages:
                send_notification(messages[choice])
                print("Message sent successfully!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Define the job scheduling
def schedule_jobs():
    print("Bot is running and connected to the webhook successfully.")
    while True:
        current_time = get_current_time()
        next_notification_time = None
        if current_time.strftime("%H:%M:%S") == "09:00:00":
            send_notification(messages[1])
            next_notification_time = current_time + timedelta(days=1)
        elif current_time.strftime("%H:%M:%S") == "15:00:00":
            send_notification(messages[2])
            next_notification_time = current_time + timedelta(days=1)
        elif current_time.strftime("%H:%M:%S") == "17:00:00":
            send_notification(messages[3])
            next_notification_time = current_time + timedelta(days=1)
        elif current_time.strftime("%a %H:%M:%S") == "Sun 09:00:00":
            send_notification(messages[4])
            next_notification_time = current_time + timedelta(days=7)
        elif current_time.strftime("%a %H:%M:%S") == "Sun 18:00:00":
            send_notification(messages[5])
            next_notification_time = current_time + timedelta(days=7)
        
        if next_notification_time:
            time_diff = next_notification_time - current_time
            total_seconds = time_diff.total_seconds()
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            print(f"Next message will be sent in {int(hours)} hours, {int(minutes)} minutes, and {int(seconds)} seconds.")
            time.sleep(30)  # Check every 30 seconds
        else:
            time.sleep(30)  # Check every 30 seconds if no next_notification_time is set

if __name__ == "__main__":
    display_menu()
    schedule_jobs()
