import socket
import select
import time
import random
import re

# UDP_IP = ""

UDP_IP = ""
IN_PORT = 5005

i = 1

buf=2048

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, IN_PORT))

# data, addr = sock.recvfrom(buf)
    # file_name = data.strip()
    # print ("File name:", file_name)
n_packet = 5000
# print("num of packet to receive",n_packet)


    # t1 = time.perf_counter_ns()
f = open("test.txt", 'wb')

received = []

check = list(range(1,int(n_packet)+1))
pointer = list(range(1,int(n_packet)+1))

# print("check list",check)
while True:
    t1 = time.perf_counter_ns()

    data, addr = sock.recvfrom(buf)
    # print("size of data received:",len(data))

    f.write(data)
    # seq = data.decode()[0]
    try:
        seq = re.search('Sequence Number: (.*)\r\n', data.decode()).group(1)
        print("received sequence number",seq)
    except AttributeError:
        seq = re.search('Sequence Number: (.*)\r\n', data.decode())
        print("received sequence number",seq)


    t2 = time.perf_counter_ns()
    time_delta = t2 - t1

    # print("seq ",seq,"i ",i)
    if data == b'END':
        print ("Received ", received)
        break
    # if int(seq) == int(pointer[0]) and len(check)!=0 and len(pointer)!=0:

    if int(seq) == int(pointer[0]):
        # print("i ",i)
        # print("pointer ",pointer)
        # print("pointer[0] ",pointer[0])

        print("send acknowledgement seq %s to server:" %seq)
        received.append(seq)
        sock.sendto(seq.encode(), addr)
        # print("received",received)
        if int(seq) in check:
            check.remove(int(seq))
            # print("check list", check)
            pointer.remove(int(seq))

        i+=1

        if len(pointer) == 0:
            break

    else:

        # print("pointer ",pointer)

        print("send acknowledgement seq to server:",int(pointer[0])-1)
        received.append(seq)
        sock.sendto(str(int(pointer[0])-1).encode(), addr)
        # print("received",received)
        if int(seq) in check:
            check.remove(int(seq))
            pointer.remove(int(seq))

            # print("check list", check)
        if len(pointer) == 0:
            break

print ("File Downloaded")
eof = "END"
sock.sendto(eof.encode(), addr)
# f.close()
#
# sock.close()
