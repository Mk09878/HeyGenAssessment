import requests
import asyncio

class TimerClient:
    def __init__(self):
        self.__server_url = 'http://127.0.0.1:5000'
        self.__backoff_time = 4  # Initial backoff time in seconds
        self.__max_attempts = 3  # Maximum number of attempts

    def start_timer(self, duration):
        payload = {'duration': duration}
        try:
            response = requests.post(f"{self.__server_url}/start-timer", json=payload)
            response.raise_for_status()  # Raise an exception for non-2xx responses
            return response.json()  # Assuming the response contains useful information
        except requests.exceptions.RequestException as e:
            print(f"Error starting timer: {e}")
            return None

    async def get_timer_status(self):
        attempts = 0
        while attempts < self.__max_attempts:
            response = requests.get(f"{self.__server_url}/status")
            if response.status_code == 200:
                status = response.json()["result"]
                if status == "pending":
                    print(f"Timer status: {status}, Trying again in {self.__backoff_time} seconds")
                    await asyncio.sleep(self.__backoff_time)
                    self.__backoff_time *= 2  # Exponential backoff
                else:
                    print(f"Timer status: {status}")
                    self.__backoff_time = 1  # Reset backoff time
                    return True
            else:
                print(f"Error: Failed to get timer status (HTTP {response.status_code})")
                await asyncio.sleep(self.__backoff_time)
                self.__backoff_time *= 2  # Exponential backoff
            attempts += 1
        
        print("Maximum number of attempts reached. Exiting...")
        return False
