import socket
import select
import sys

# Connect to the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 12345))

# Set up reader and writer
reader = s.makefile('r')
writer = s.makefile('w')

# Receive and display welcome message
welcome = reader.readline()
print(welcome.strip())

try:
    while True:
        server_messages = []

        # Use select to detect when server is ready for input
        while True:
            ready, _, _ = select.select([s], [], [], 0.1)  # Wait for server data
            
            if not ready:  # No more data, assume server is waiting for input
                break  

            prompt = reader.readline()
            if not prompt:
                raise ConnectionResetError  # Server disconnected
            
            server_messages.append(prompt.strip())

        # Print all received messages
        if server_messages:
            print("\n".join(server_messages))

        # Get user input and send it to the server
        num = input("Your Input: ")
        writer.write(f"{num}\n")
        writer.flush()

except (ConnectionResetError, BrokenPipeError):
    print("Disconnected from server.")

finally:
    writer.close()
    reader.close()
    s.close()
