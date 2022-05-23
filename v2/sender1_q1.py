import socket
import time
import sys
import os
import math

UDP_IP = ""
# UDP_PORT = 12001
# UDP_IP = ""
UDP_PORT = int(input("Enter the Port number on which your receiver is running: "))

buf = 1001
file_name = "message.txt"
# n_packet = 6
p_size = 1000
n_packet = int(os.path.getsize(file_name)/p_size)*8+1  #byte

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.bind(('', UDP_PORT))
sock.connect((UDP_IP,UDP_PORT))


print("server is ready to send file %s" % file_name)

print ("Sending Total number of packet %s ..." % str(n_packet).encode())
# sock.send(str(n_packet).encode())
check = list(range(1,int(n_packet)+1))
print("check list",check)

sent = []
f = open(file_name, "r")
time_table = [0]*(n_packet+1)
RTT = [0]*(n_packet+1)
rec = [0]*(n_packet+1)
size = [0]*(n_packet+1)

data = f.read(buf)

def get_last_non_zero_idx(my_list):
    return max([index for index, el in enumerate(my_list) if el])


while (len(check)!=0):
    for i in range(1,n_packet+1):
    # for i in check:
    # for i in [1,2,3,5,6,4]:
        # print("processing seq",i)
        l = []
        #append sequence number
        l.append(str(i)+str("|"))
        l.append(data)

        data = ''.join(l)
        size[i]=len(data)

        t1 = time.time()
        time_table[i]=t1
        # print("time_table[i]",time_table[i])
        if(sock.send(data.encode())):
            data = f.read(buf)
            time.sleep(0.02) # Give receiver a bit time to save

            ack = 0
            # while ack != i:


            try:
                ack = sock.recv(buf)
                if ack == b'END':
                    print ("full package transmitted")
                    break
                else:
                    sock.settimeout(5)

                    # print("acknowledgement received:",int(ack),"from",str((UDP_IP,UDP_PORT)))

                    # print("\n")

                    print("Current Window: ",i)
                    print("Sequence Number of Packet Sent: ",i)
                    print("Acknowledgment Number Received: ",int(ack))
                    # print("\n")


                    if int(i) in check:
                        check.remove(int(i))
                        sent.append(i)
                    if int(ack) >= i:
                    # if int(ack) in check:
                    #     check.remove(int(ack))
                    # ack = int(ack)
                        t2 = time.time()
                        # print("t2",t2)
                        rec[i] = t2
                        RTT[i] = t2 - time_table[i]
                        # print("RTT[i]",RTT[i])
                        #
                        # print("check",check)
                        # sent.append(i)

                        for j in range(1,max(sent)+1):
                            if  RTT[j] == 0:
                                # print("enter RTT post update for j ",j)
                                if j in sent:
                                    # print(rec[i])
                                    # print(time_table[i])
                                    RTT[j] = rec[i]- time_table[i]
                                    # print(RTT[j])

                    # if int(ack) > i:
                    #
                    #     t2 = time.time()
                    #
                    #     print("check",check)
                    #     sent.append(i)

            except socket.timeout as err:
                print ('caught a timeout')

# print ("sequence sent: ", sent)
size = [(float(x)) for x in size]
RTT = [(float(x)) for x in RTT]

avg_thu = sum(size)/sum(RTT)
avg_del = sum(RTT)/len(RTT)
print ("average throughput: ", avg_thu)
print ("average delay: ", avg_del)
print ("Performance : ", math.log(avg_thu,10)-math.log(avg_del,10))



f.close()
sock.close()
