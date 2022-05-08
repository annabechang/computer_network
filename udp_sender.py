import socket
import time
import sys
import os

UDP_IP = ""
# UDP_PORT = 12001
# UDP_IP = ""
UDP_PORT = 5005
buf = 4068
file_name = "test.txt"


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', UDP_PORT))

PACKET_COUNT = 0
sequence_list = []


# print("server is ready to send file %s" % file_name)
# f = open(file_name)
# f.seek(0, os.SEEK_END)
# print('Size of file is', f.tell(), 'bytes')


# sock.sendto(file_name.encode(), (UDP_IP, UDP_PORT))


while True:
    # print ("Sending %s ..." % file_name)
    dt = time.time()
    message, clientAddress = sock.recvfrom(2048)
    print("server received:",str(message),"from",str(clientAddress))

    if message == b'END!':
        print ("Received " + str(PACKET_COUNT - 1))
        break
    else:
        sequence_list.append(int.from_bytes(message, byteorder='big'))
    PACKET_COUNT = PACKET_COUNT + 1

unique_sequences = []
count = 0

for i in range(len(sequence_list)-1):
    if sequence_list[i] + 1 == sequence_list[i+1]:
        if unique_sequences == []:
            unique_sequences.append([sequence_list[i]])
            count = count + 1
        elif sequence_list[i] != unique_sequences[-1][-1]:
            unique_sequences.append([sequence_list[i]])
            count = count + 1
        if sequence_list[i+1] != unique_sequences[-1]:
            unique_sequences[-1].extend([sequence_list[i+1]])
print("sequence list", sequence_list)
print("Out of order packets:", (len(unique_sequences)-1))

    # f = open(file_name, "r")
    # data = f.read(buf)
    # d_l = len(data)
    # while(data):
    #     if(sock.sendto(data.encode(), clientAddress)):
    #         data = f.read(buf)
    #         time.sleep(0.02) # Give receiver a bit time to save


# f.close()
sock.close()
