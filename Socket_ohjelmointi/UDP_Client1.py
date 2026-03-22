import socket as sk

try:
    s = sk.socket(sk.AF_INET, sk.SOCK_DGRAM, sk.IPPROTO_UDP)
except sk.error:
    print("Cannot create socket, quit")
    exit()

while True:
    try:
        m = input("Msg to server: ")
        s.sendto(bytearray(m, encoding="ascii"), ("localhost", 4444))
        try:
            m, addr = s.recvfrom(1000)
            print(m.decode("ascii"))
        except sk.error:
            print("Something is wrong")
            break
    except KeyboardInterrupt: break

s.close()