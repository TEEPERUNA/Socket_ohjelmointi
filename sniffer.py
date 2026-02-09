import socket
import struct

ETH_P_ALL = 0x03
rs = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ALL))
rs.bind(("enp0s3", 0))
print(rs.getsockname())

while True:
    raw, addr = rs.recvfrom(65535)
    dst, src, ethtype = struct.unpack('!6s6s2s', raw[:14])
    print(dst, src, ethtype)
    if ethtype == b'\x08\x00':
        print("IPv4 packet")
        pass

    break