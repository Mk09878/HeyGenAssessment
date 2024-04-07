<a name="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">HeyGen Assessment</h3>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#usage">Usage</a></li>
      </ul>
    </li>
    <li><a href="#improvements">Improvements</a></li>
  </ol>
</details>


## About The Project

This project comprises of 2 components:

1. Server
2. Client

### Server
The Server is a Python Flask application which has 2 endpoints:

#### Start Timer

- **Endpoint:** `/start-timer`
- **Method:** POST
- **Description:** Initiates a timer for a specified duration.
  - Request Body:
    ```json
    {
        "duration": 10
    }
    ```
  - Responses:
    - 200 OK: Timer started successfully.
      ```json
      {
          "message": "Timer started for 10 seconds"
      }
      ```
    - 400 Bad Request: Indicates an error with the request.
      - If no duration is provided:
        ```json
        {
            "error": "No duration provided"
        }
        ```
      - If the provided duration is invalid:
        ```json
        {
            "error": "Invalid duration value"
        }
        ```

#### Get Timer Status

- **Endpoint:** `/status`
- **Method:** GET
- **Description:** Retrieves the status of the timer.
  - Responses:
    - 200 OK: Returns the status of the timer.
      - If the timer is running:
        ```json
        {
            "result": "pending"
        }
        ```
      - If the timer has completed:
        ```json
        {
            "result": "completed"
        }
        ```

    - 404 Not Found: Indicates that the timer status endpoint is not available.

### Client

The client is responsible for calling the server endpoints.

It exposes 2 methods:

### start_timer

The start_timer() method is synchronous.
This method sends a POST request to the Timer Server's /start-timer endpoint.
Since the operation of starting a timer is a simple request-response operation and does not involve any waiting or concurrency, it can be handled synchronously without blocking the execution flow.
The method waits for the server's response and returns it synchronously, allowing the caller to handle the response immediately.

### get_timer_status

The get_timer_status() method has the following features:

Exponential Backoff:

To avoid flooding the server with too many requests and to handle network issues gracefully, the method implements exponential backoff.

Initially, it waits for a fixed duration (e.g., 4 seconds) before retrying the request.

If the timer status is still pending after the first attempt, it increases the wait time exponentially for each subsequent attempt (e.g., doubling the wait time with each retry).

This approach prevents unnecessary delays in getting the status and reduces the load on the server by gradually increasing the time between retries.

Retry Mechanism:

The method retries the request until the timer status is retrieved successfully or the maximum number of attempts is reached.
It handles potential errors such as network issues, server timeouts, or server errors gracefully by retrying the request with exponential backoff.


## Getting Started

### Prerequisites

You need to have python installed on your system

### Installation

To manage project dependencies and isolate them from other projects on your system, it's recommended to use a Python virtual environment. Follow the steps below to create and activate a virtual environment for this project:

1. Install virtualenv (if not already installed):

    ```
    pip install virtualenv
    ```

2. Create a virtual environment:

    ```
    virtualenv venv
    ```

    Replace venv with the desired name of your virtual environment.

3. Activate the virtual environment:

    * Windows:

    ```
    venv\Scripts\activate
    ```

    * Linux/ macOS

    ```
    source venv/bin/activate
    ```

4. Install dependencies:

    ```
    pip install -r requirements.txt
    ```

5. Deactivate the virtual environment:

    ```
    deactivate
    ```

## Usage

1. Run the server:

    Navigate to server directory and run
    ```
    python app.py
    ```

    OR

    ```
    python Server/app.py
    ```

    You can now run the manual_test.py file

    ```
    python manual_test.py
    ```

    This file simulates hitting the 2 server endpoints through the client

    You could also send curl requests to the server directly if desired


2. Run integration test:

    You may need to stop the server before running the integration test

    ```
    python -m unittest discover .\tests\
    ```

## Improvements

We could get rid of the client and use a pub-sub pattern. The workflow would look like this: 
The user uploads the video. The video translation service would send messages to a queue. We can have a service which polls the queue and displays notifications to the user on the UI. It could also send notifications in terms of emails.

Advantages: 
1. We can get rid of the client completely.
2. We do not have to worry about the server becoming overloaded because of constant requests to check status.
3. By adjusting the polling frequency, we can decide how quickly we would want to inform the clients that their video is ready.

If we want to keep using this pattern, introduction of throttling to the server could be a way of making sure that it doesnt get overwhelmed. There could be multiple strategies for doing this. We could have the user pass an API key to the client. The server can then throttle based on that API key. 