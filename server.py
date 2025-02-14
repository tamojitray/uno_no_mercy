import eventlet
eventlet.monkey_patch()

from flask import Flask, request
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

# Store all calculations with usernames
all_results = []

@socketio.on('connect')
def handle_connect():
    username = request.args.get("username")  # Get username from client
    if not username:
        print(f"Client connected: {request.sid} (No name provided)")
        return

    print(f"Client connected: {username}")

    # Send full list of past results to the newly connected client
    socketio.emit("update_results", {"results": all_results}, room=request.sid)

@socketio.on('add_numbers')
def handle_add_numbers(data):
    username = data.get("username", "Anonymous")  # Default to Anonymous if no name
    num1 = data.get("num1", 0)
    num2 = data.get("num2", 0)
    result = num1 + num2

    # Store the result with the username
    entry = f"{username}: {num1} + {num2} = {result}"
    all_results.append(entry)
    
    print(f"New Calculation by {username}: {entry}")

    # Broadcast updated results to all clients
    socketio.emit("update_results", {"results": all_results})

@socketio.on('disconnect')
def handle_disconnect():
    print(f"Client disconnected: {request.sid}")

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000)
