# Raw socket ICMP ping example (student ID in payload + correct identifier)
import socket as sc
import threading
import time

# *** CONFIG ***
# Oleta että sun opiskelijanumero on e2301760
# Option Data = ASCII "e2301760"
# Identifier = viimeiset 4 numeroa = 1760 -> 0x1760
STUDENT_ID = b"e2301760"
IDENTIFIER = 0x1760  # 1760 desimaalina -> 0x1760 heksana

sequence = 0


def checksum(packet: bytearray) -> int:
    # Kopio, ettei sotketa alkuperäistä pakettia
    data = bytearray(packet)
    plen = len(data)
    if plen % 2 == 1:
        data.append(0)
        plen += 1

    s = 0
    for i in range(0, plen, 2):
        s += (data[i] << 8) + data[i + 1]

    # Foldataan 32-bittinen 16-bittiseksi
    s = (s >> 16) + (s & 0xFFFF)
    s = (s >> 16) + (s & 0xFFFF)

    return 0xFFFF - s


def build_icmp_packet(seq: int) -> bytearray:
    """
    Rakentaa ICMP Echo Request -paketin:
    - Type      = 8
    - Code      = 0
    - Checksum  = laskettu
    - Identifier= IDENTIFIER (0x1760)
    - Sequence  = seq (0..65535)
    - Data      = STUDENT_ID (ASCII, 8 oktettia)
    """
    # ICMP header = 8 tavua, sen perään data
    packet = bytearray(8 + len(STUDENT_ID))

    # Type + Code
    packet[0] = 8   # Echo request
    packet[1] = 0   # Code 0

    # Checksum aluksi 0
    packet[2] = 0
    packet[3] = 0

    # Identifier (2 tavua, big endian)
    packet[4] = (IDENTIFIER >> 8) & 0xFF
    packet[5] = IDENTIFIER & 0xFF

    # Sequence (2 tavua, big endian)
    packet[6] = (seq >> 8) & 0xFF
    packet[7] = seq & 0xFF

    # Data = opiskelijanumero ASCII
    packet[8:8 + len(STUDENT_ID)] = STUDENT_ID

    # Lasketaan checksum koko ICMP-viestille
    csum = checksum(packet)
    packet[2] = (csum >> 8) & 0xFF
    packet[3] = csum & 0xFF

    return packet


def send(s: sc.socket):
    seq = 0
    while True:
        time.sleep(1)
        seq += 1
        if seq >= 2**16:
            seq = 1  # pidetään 0x0000 välistä, eka on 0x0001

        packet = build_icmp_packet(seq)
        print(f"Send (seq={seq}): {packet}")
        s.sendto(packet, (target_ip, 0))


def recv(s: sc.socket):
    while True:
        d = s.recvfrom(65535)
        src_ip = d[1][0]
        if src_ip != target_ip:
            continue

        # IPv4-header oletetaan 20 tavun mittaiseksi (ilman optioita)
        icmp_part = d[0][20:]
        print(f"Recv from {src_ip}: {icmp_part}")


# Luodaan raw-socket ICMP:lle
s = sc.socket(sc.AF_INET, sc.SOCK_RAW, sc.IPPROTO_ICMP)
s.bind(("", 0))

target_ip = input("Address to ping: ")

t1 = threading.Thread(target=recv, args=(s,), daemon=True)
t2 = threading.Thread(target=send, args=(s,), daemon=True)

t1.start()
t2.start()

# Estetään pääohjelmaa kuolemasta
while True:
    time.sleep(1)
