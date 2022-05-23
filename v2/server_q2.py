import socket
import time
import sys
import os
import math

UDP_IP = ""
# UDP_PORT = 12001
# UDP_IP = ""
UDP_PORT = int(input("Enter the Port number on which your receiver is running: "))
buf = 4096
file_name = "message.txt"
n_packet = 20
win_size = 3
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.bind(('', UDP_PORT))
sock.connect((UDP_IP,UDP_PORT))


print("server is ready to send file %s" % file_name)

print ("Sending Total number of packet %s ..." % str(n_packet).encode())
# sock.send(str(n_packet).encode())
check = list(range(1,int(n_packet)+1))
# print("check list",check)
sent = []
received = []
f = open(file_name, "r")
time_table = [0]*100
RTT = [0]*100
rec = [0]*100
size = [0]*100

data = f.read(buf)
def get_last_non_zero_idx(my_list):
    return max([index for index, el in enumerate(my_list) if el])

while (len(check)!=0):
    for i in range(1,n_packet, win_size):
    # for i in check:

        for j in range(i,i+win_size):

            if j >= n_packet+1:
                break
            else:
                print("processing seq",j)
                l = []
                #append sequence number
                l.append(str(j)+str("|"))
                l.append(data)

                data = ''.join(l)
                size[i]=len(data)                # print("data header: ", data[:20])
                # print("sending data of sequence number: ",data[0])
        #         # while(data):.
                t1 = time.time()
                time_table[i]=t1
                if(sock.send(data.encode())):
                    data = f.read(buf)
                    time.sleep(0.02) # Give receiver a bit time to save

                    ack = 0
                    # while ack != i:

                    while (j not in received):

                        try:
                            ack = sock.recv(buf)

                            print("Current Window: ",range(j,j+win_size))
                            print("Sequence Number of Packet Sent: ",j)
                            print("Acknowledgment Number Received: ",int(ack))


                            if ack == b'END':
                                print ("full package transmitted")
                                break
                            else:
                                sock.settimeout(5)

                                print("acknowledgement received:",int(ack),"from",str((UDP_IP,UDP_PORT)))


                                if int(ack) in check:
                                    check.remove(int(ack))
                                    sent.append(i)
                                    received.append(j)


                                if int(ack) >= j:
                                    t2 = time.time()
                                    rec[j] = t2
                                    RTT[j] = t2 - time_table[i]

                                    for k in range(1,max(sent)+1):


                                        if  RTT[k] == float(0):
                                            if k in sent:
                                                RTT[j] = rec[j]- time_table[k]


                                if j == n_packet:
                                    break


                        except socket.timeout as err:
                            print ('caught a timeout')

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
