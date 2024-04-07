from flask import Flask, jsonify, request
import threading
import time

app = Flask(__name__)

# Variable to track whether the timer is running
timer_running = False

def start_timer(duration):
    global timer_running
    timer_running = True
    time.sleep(duration)
    timer_running = False

def validate_duration(duration):
    try:
        duration = float(duration)
        if duration <= 0:
            raise ValueError
        return duration
    except ValueError:
        return None

@app.route('/start-timer', methods=['POST'])
def start_timer_endpoint():
    global timer_thread
    global timer_running
    if timer_running:
        return jsonify({"message": "Timer is already running"}), 400

    duration = request.json.get('duration')
    if duration is None:
        return jsonify({"error": "No duration provided"}), 400

    duration = validate_duration(duration)
    if duration is None:
        return jsonify({"error": "Invalid duration value"}), 400

    timer_thread = threading.Thread(target=start_timer, args=(duration,))
    timer_thread.start()
    return jsonify({"message": f"Timer started for {duration} seconds"}), 200

@app.route('/status', methods=['GET'])
def get_status():
    global timer_running
    return jsonify({"result": "pending" if timer_running else "completed"})

if __name__ == '__main__':
    app.run(debug=True)
