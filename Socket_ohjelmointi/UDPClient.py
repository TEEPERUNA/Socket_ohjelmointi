import socket
import threading

SERVER_IP = "localhost"
SERVER_PORT = 44444
BUFFER_SIZE = 1000

running = True

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print("Cannot open socket, quit")
    exit()


def receive_messages():
    global running
    while running:
        try:
            data, addr = s.recvfrom(BUFFER_SIZE)
            print("\n" + data.decode("ascii"))
        except socket.error:
            break


# Start receiver thread
receiver = threading.Thread(target=receive_messages, daemon=True)
receiver.start()

print("UDP group chat client started")
print("Type messages and press Enter")
print("Type BYE to leave")

# Send join message so server learns this client immediately
s.sendto("joined the chat".encode("ascii"), (SERVER_IP, SERVER_PORT))

while True:
    try:
        msg = input("> ")

        s.sendto(msg.encode("ascii"), (SERVER_IP, SERVER_PORT))

        if msg == "BYE":
            running = False
            break

    except KeyboardInterrupt:
        s.sendto("BYE".encode("ascii"), (SERVER_IP, SERVER_PORT))
        running = False
        break

s.close()
print("Client closed")