import socket
import time
import sys
import os
import math


UDP_IP = ""
# UDP_PORT = 5005
# UDP_IP = ""
UDP_PORT = int(input("Enter the Port number on which your receiver is running: "))
buf = 1001
file_name = "message.txt"
p_size = 1000
n_packet = int(os.path.getsize(file_name)/p_size)+1
win_size = 1
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
time_table = [0]*(n_packet+1)
RTT = [0]*(n_packet+1)
rec = [0]*(n_packet+1)
size = [0]*(n_packet+1)
estimatedRTT = [0]*(n_packet+1)
DevRTT= [0]*(n_packet+1)
data = f.read(buf)
ssthresh = 8
time_out=5

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

def CountFrequency(my_list):

    # Creating an empty dictionary
    freq = {}
    for item in my_list:
        if (item in freq):
            freq[item] += 1
        else:
            freq[item] = 1

    max_f = max(freq.values())
    return max_f

i = 1
while (n_packet in check):
    while i <= n_packet:

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
        print("Current Window: ",range(i,bound-1))

        for j in range(i,bound):
            # print("j", j)
            # print("i+win_size ", i+win_size)

            if j >= n_packet+1:
                break
            if len(check) == 0:
                break
            else:
                sending(j, data)


        buff_data = []
        comp  = bound - i
        # ran = ((comp) if (comp> 0) else 1)
        if comp> 0:
            ran = comp
        else:
            ran = 1
        print("ran",ran)
        if ran != 0:
            for m in range(0,ran):
                try:
                    estimatedRTT[1] = RTT[1]

                    sock.settimeout(time_out)

                    ack = sock.recv(buf)

                    if int(ack) <= j:
                        t2 = time.time()
                        rec[int(ack)] = t2
                        # print(t2)
                        # print(time_table[j])
                        val = float(t2) - float(time_table[j])
                        # print(val)
                        # print(RTT[j])
                        RTT[int(ack)] = (val)
                    estimatedRTT[int(ack)] = 0.875*estimatedRTT[int(ack)-1]+0.125*RTT[int(ack)]
                    print("index int(ack)",int(ack))
                    print("estimatedRTT",estimatedRTT[int(ack)])
                    DevRTT[int(ack)] = 0.75*DevRTT[int(ack)-1]+0.25*abs(RTT[int(ack)-1]-estimatedRTT[int(ack)])
                    print("DevRTT",DevRTT[int(ack)])
                    time_out = estimatedRTT[int(ack)]+4*DevRTT[int(ack)]
                    print("time_out",time_out)

                    buff_data.append(int(ack))
                    # print("buff_data",buff_data)
                    count_duplicate = CountFrequency(buff_data)


                    t2 = time.time()
                    rec[i] = t2
                    # print("1")
                    if max(buff_data)>=n_packet:
                        # print("2")
                        m = n_packet
                        break
                except socket.timeout as err:
                    print ('caught a timeout')
                    lost +=1
                    sending(ack, data)
                    ack = sock.recv(buf)

                    if int(ack) <= j:
                        t2 = time.time()
                        rec[int(ack)] = t2
                        # print(t2)
                        # print(time_table[j])
                        val = float(t2) - float(time_table[j])
                        # print(val)
                        # print(RTT[j])
                        RTT[int(ack)] = (val)*1000


                        estimatedRTT[int(ack)] = 0.875*estimatedRTT[int(ack)-1]+0.125*RTT[int(ack)]
                        print("index int(ack)",int(ack))
                        print("estimatedRTT",estimatedRTT[int(ack)])
                        DevRTT[int(ack)] = 0.75*DevRTT[int(ack)-1]+0.25*abs(RTT[int(ack)-1]-estimatedRTT[int(ack)])
                        print("DevRTT",DevRTT[int(ack)])
                        time_out = estimatedRTT[int(ack)]+4*DevRTT[int(ack)]
                        print("time_out",time_out)

                    buff_data.append(int(ack))
                    # print("buff_data",buff_data)
                    count_duplicate = CountFrequency(buff_data)

                    # print("3")
            if count_duplicate>=3:
                # print("4")
                print ('triple ack')
                lost +=1
                sending(int(max(buff_data)), data)


        while (j not in received):

            try:


                ack = max(buff_data)
                if ack == b'END':
                    print ("full package transmitted")
                    break
                else:

                    print("acknowledgement received:",int(ack))



                    if int(ack) in check:
                        check.remove(int(ack))


                        sent.append(j)

                        received.append(j)
                    #
                    # if int(ack) >= j:
                    #
                    #     # print(t2)
                    #     # print(time_table[j])
                    #     val = float(t2) - float(time_table[j])
                    #     # print(val)
                    #     # print(RTT[j])
                    #     RTT[j] = (val)
                    #
                    #     # print("1")
                    #     for k in range(1,max(sent)+1):
                    #
                    #         if  RTT[k] == float(0):
                    #             if k in sent:
                    #                 RTT[j] = rec[j]- time_table[k]


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


        # print("i origin",i)
        # i ==bound
        # print("i +bound",i)
        print("win_size origin",win_size)
        if win_size*2 <(ssthresh+1):
            win_size+=win_size
            print("win_size *2",win_size)

        elif win_size > (ssthresh-1) or lost == 1:
            win_size+=1
            # print("win_size +1",win_size)

        elif lost == 2:
            win_size = 1
            ssthresh = ssthresh/2
            # print("win_size =1",win_size)


        # if (lost <4) and (lost != 0):
        #     win_size+=1
        if len(check) == 0:
            break
        # else:
        #     win_size == 1



size = [(float(x)) for x in size]
RTT = [(float(x)) for x in RTT]
# print(size)
# print(RTT)
avg_thu = sum(size)*8/sum(RTT)
avg_del = (sum(RTT)/len(RTT))
print ("average throughput: ", avg_thu," bits per second")
print ("average delay: ", avg_del," milliseconds")
print ("Performance : ", math.log(avg_thu,10)-math.log(avg_del,10))

f.close()

sock.close()
