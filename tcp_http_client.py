import socket as sc

s = sc.socket(sc.AF_INET, sc.SOCK_STREAM)
try:
    s.connect(("www.cc.puv.fi", 80))
except sc.error:
    print("connection failed, quit")
    exit()

s.send(b"GET /~gc/index.html HTTP/1.1\r\nHost: www.cc.puv.fi\r\n\r\n")
msg = s.recv(2048)
print(msg.decode("ascii"))
s.close()
