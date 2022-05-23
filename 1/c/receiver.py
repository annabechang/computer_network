import socket
import select
import time
import random
import re

# UDP_IP = ""

UDP_IP = ""
IN_PORT = 5005
timeout = 1
count = 0
sleep_t = (timeout * 2 ** count +
                 random.uniform(0, 1))

buf=1000
tar_size = 3000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.bind((UDP_IP, IN_PORT))

data = "ping"
sock.sendto(data.encode('ascii'), (UDP_IP, IN_PORT))

data, addr = sock.recvfrom(buf)
# file_name = data.strip()
# print ("File name:", file_name)
n_packet = data.decode()
print("num of packet to receive",n_packet)



# t1 = time.perf_counter_ns()
f = open("test.txt", 'wb')
#
#
#
# # try:



received = []

check = list(range(1,int(n_packet)+1))
print("check list",check)
while True:
#     print("received %: ", round(f.tell()/tar_size*100))
    t1 = time.perf_counter_ns()
#
#
    # ready = select.select([sock], [], [], timeout)
    # #     print("ready",ready)
    # if ready[0]:
    #
    #
    data, addr = sock.recvfrom(buf)
    print("size of data received:",len(data))

    f.write(data)
    # seq = data.decode()[0]
    try:
        seq = re.search('Sequence Number: (.*)\r\n', data.decode()).group(1)
        print("received sequence number",seq)
    except AttributeError:
        seq = re.search('Sequence Number: (.*)\r\n', data.decode())
        print("received sequence number",seq)

    try:
        win = re.search('Window: (.*)\r\n', data.decode()).group(1)
        print("received window size:",win)
    except AttributeError:
        win = re.search('Window: (.*)\r\n', data.decode())
        print("received window size:",win)


    t2 = time.perf_counter_ns()
    time_delta = t2 - t1

    if data == b'END':
        print ("Received ", received)
        break

    else:
        print("send acknowledgement seq %s to server:" %seq)
        # print("window size %s to server:" %win)

        # x = random.randrange(1,5)
        # print("x",x)
        # if x>=2:
        sock.sendto(seq.encode(), (UDP_IP, IN_PORT))
        received.append(seq)
        print("received",received)
        if int(seq) in check:
            check.remove(int(seq))
            print("check list", check)

        # else:
        #     time.sleep(5)
        #     print("no acknowledgement sent")
        #     sock.sendto(seq.encode('ascii'), (UDP_IP, IN_PORT))
        #     received.append(seq)
        #     print("received",received)
        #     if int(seq) in check:
        #         check.remove(int(seq))
        #         print("check list", check)
        #     continue



#         throughput = (f.tell()) / time_delta
#         print("f.tail",f.tell(), "tar size",tar_size)
#         # print(time_delta,throughput)
#     else:
#         print("break")
#         break
#
#
# print(f"Time elapsed: {time_delta} ms" )
# print(f"Throughput: {throughput} bps")
# print('Size of file is', f.tell(), 'bytes')

    # f.close()
    # sock.close()
# except socket.timeout:
#     print("time out")
#     # time.sleep(sleep_t)
#     count+=1




print ("File Downloaded")
# f.close()
#
# sock.close()
