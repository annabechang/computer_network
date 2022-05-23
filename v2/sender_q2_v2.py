import socket
import time
import sys
import os
import math


UDP_IP = ""
# UDP_PORT = 12001
# UDP_IP = ""
UDP_PORT = int(input("Enter the Port number on which your receiver is running: "))
# UDP_PORT = 5005

buf = 4096
file_name = "message.txt"

win_size = 3
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.bind(('', UDP_PORT))
sock.connect((UDP_IP,UDP_PORT))


print("server is ready to send file %s" % file_name)

# sock.send(str(n_packet).encode())
# print("check list",check)

sent = []
received = []
f = open(file_name, "r")
# n_packet = 10
p_size = 1000
n_packet = int(os.path.getsize(file_name)/p_size)+1
print("n_packet",n_packet)

win_size = 3
time_table = [0]*(n_packet+1)
RTT = [0]*(n_packet+1)
rec = [0]*(n_packet+1)
size = [0]*(n_packet+1)
data = f.read(buf)
check = list(range(1,int(n_packet)+1))

# print ("Sending Total number of packet %s ..." % str(n_packet).encode())

def get_last_non_zero_idx(my_list):
    return max([index for index, el in enumerate(my_list) if el])

def sending(seq, data):
    l = [] # processing the data to be sent
    #append sequence number
    # print("len data",len(data))
    l.append(str(seq)+str("|"))
    l.append(data)

    data = ''.join(l)
    size[i]=len(data)
    # print("size[i]",len(data))
#         #
    # print("data header: ", data[:20])
    # print("sending data of sequence number: ",data[0])
#         # while(data):.
    t1 = time.time()
    if time_table[i]==0:
        time_table[i]=t1

    if(sock.send(data.encode())):
        # data = f.read(p_size)
        # time.sleep(0.02) # Give receiver a bit time to save


        # while ack != i:
        print("Sequence Number of Packet Sent: ",j)

i = 1
while (n_packet in check):

    # print("check",check)
    while i <= n_packet:
        # print("i,npacket",i,n_packet)
    # for i in range(1,n_packet, win_size):
    # for i in check:
        # print("i ",i)
        lost= 0
        bound = i+win_size
        if bound<=n_packet+1:
            bound

        else:
            bound = n_packet+1

        # print("win_size ", win_size)

        for j in range(i,bound):
            # print("j", j)
            # print("i+win_size ", i+win_size)
            print("Current Window: ",range(j,bound-1))

            if j >= n_packet+1:
                break
            if len(check) == 0:
                break
            else:
                sending(j, data)

        # print(i,j,bound,win_size)
        buff_data = []
        ran = bound - i if bound >= bound - i>0 else 1
        # print("ran",ran)
        if ran != 0:
            for m in range(0,ran):
                # print(m,ran)
                try:
                    ack = sock.recv(buf)
                    buff_data.append(int(ack))
                    # print("ack = ", ack)
                    # print("Acknowledgment Number Received: ",buff_data)
                    # print(buff_data[-1],n_packet)
                    if buff_data[-1]>=n_packet:
                        m = n_packet
                        break
                except socket.timeout as err:
                    print ('caught a timeout')
                    lost +=1
                    sending(ack, data)

        while (j not in received):

            try:

                ack = buff_data[-1]
                if ack == b'END':
                    print ("full package transmitted")
                    break
                else:
                    sock.settimeout(5)

                    print("acknowledgement received:",int(ack))



                    if int(ack) in check:
                        check.remove(int(ack))


                        sent.append(j)

                        received.append(j)
                        # print("received",received)

                    if int(ack) >= j:
                        t2 = time.time()
                        rec[i] = t2
                        # print(t2)
                        # print(time_table[j])
                        val = float(t2) - float(time_table[j])
                        # print(val)
                        # print(RTT[j])
                        RTT[j] = (val)
                        # print("1")
                        for k in range(1,max(sent)+1):


                            if  RTT[k] == float(0):
                                if k in sent:
                                    RTT[j] = rec[j]- time_table[k]
                        # print("2")
                    # print("i1",i,ack)

                    i=ack+1
                    # print("i2",i,ack)
                    if j >= n_packet:
                        # print("j",j)
                        break
                    if i >= n_packet:
                        # print("i",i)
                        break
                # print("win_size +=win_size",win_size)
            except socket.timeout as err:
                print ('caught a timeout')
                lost +=1
                sending(ack, data)


        # i ==bound
        if (lost <4) and (lost != 0):
            win_size+=1
        if len(check) == 0:
            break
        else:
            win_size == 1



size = [(float(x)) for x in size]
RTT = [(float(x)) for x in RTT]
# print(size)
# print(RTT)
avg_thu = sum(size)/sum(RTT)
avg_del = sum(RTT)/len(RTT)
print ("average throughput: ", avg_thu)
print ("average delay: ", avg_del)
print ("Performance : ", math.log(avg_thu,10)-math.log(avg_del,10))

f.close()

sock.close()
