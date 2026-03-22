import socket

SERVER_PORT = 44444
BUFFER_SIZE = 1000

clients = set()

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print("Cannot create socket")
    exit()

s.bind(("", SERVER_PORT))
print(f"UDP chat server is ready on port {SERVER_PORT}")

while True:
    try:
        data, caddr = s.recvfrom(BUFFER_SIZE)
        message = data.decode("ascii").strip()

        # Add new client automatically
        if caddr not in clients:
            clients.add(caddr)
            print(f"New client joined: {caddr}")

        # Client leaves
        if message == "BYE":
            if caddr in clients:
                clients.remove(caddr)
            print(f"Client left: {caddr}")

            leave_msg = f"{caddr} left the chat"
            for client in clients:
                s.sendto(leave_msg.encode("ascii"), client)

            continue

        print(f"[{caddr}]: {message}")

        # Send message to all other clients
        forward_msg = f"{caddr[0]}:{caddr[1]} says: {message}"
        for client in clients:
            if client != caddr:
                s.sendto(forward_msg.encode("ascii"), client)

    except socket.error:
        print("recvfrom/sendto error")