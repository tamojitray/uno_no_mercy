import eventlet
eventlet.monkey_patch()

from flask import Flask, request
from flask_socketio import SocketIO


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

@socketio.on('connect')
def handle_connect():
    print("Client connected", request.sid)

@socketio.on('add_numbers')
def handle_add_numbers(data):
    print(data)
    num1 = data.get("num1", 0)
    num2 = data.get("num2", 0)
    result = num1 + num2
    print(f"Received numbers: {num1}, {num2}. Sending result: {result}")
    socketio.emit("result", {"result": result}, room=request.sid)

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000)
