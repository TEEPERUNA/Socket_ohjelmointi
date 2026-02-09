import socket as sc
import struct
rs = sc.socket(sc.PF_PACKET, sc.SOCK_RAW, sc.htons(0x0800))
rs.bind(("enp0s3", sc.htons(0x0800)))

pkt = struct.pack("!6s6s2s", b'\x01\x0C\xCD\x01\x00\x00',
			b'\x00\x01\x02\x03\x04\x05',b'\x88\xb8')

rs.send(pkt + b"HELLO")