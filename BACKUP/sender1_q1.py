import socket
import time
import sys
import os

UDP_IP = ""
# UDP_PORT = 12001
# UDP_IP = ""
UDP_PORT = int(input("Enter the Port number on which your receiver is running: "))

buf = 1000
file_name = "test.txt"
n_packet = 6

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.bind(('', UDP_PORT))
sock.connect((UDP_IP,UDP_PORT))


print("server is ready to send file %s" % file_name)

print ("Sending Total number of packet %s ..." % str(n_packet).encode())
# sock.send(str(n_packet).encode())
check = list(range(1,int(n_packet)+1))
print("check list",check)
mylist=[]
sent = []
f = open(file_name, "r")
time_table = [0]*100
RTT = [0]*100

data = f.read(buf)

while (len(check)!=0):
    # for i in range(1,n_packet+1):
    # for i in check:
    for i in [1,2,3,5,6,4]:
        print("processing seq",i)
        l = []
        #append sequence number
        l.append(str(i)+str("|"))
        l.append(data)

        data = ''.join(l)
        #
        # print("data header: ", data[:20])
        # print("sending data of sequence number: ",data[0])
        # print("size of the data sent:",len(data))
#         # while(data):.
        t1 = time.time()
        time_table[i]=t1
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

                    print("acknowledgement received:",int(ack),"from",str((UDP_IP,UDP_PORT)))

                    if int(i) in check:
                        check.remove(int(i))
                    if int(ack) == i:
                    # if int(ack) in check:
                    #     check.remove(int(ack))
                    # ack = int(ack)
                        t2 = time.time()
                        RTT[i] = t2 - time_table[i]
                        mylist.append(RTT)

                        print("check",check)
                        sent.append(i)
                    if int(ack) >= i:
                    # if int(ack) in check:
                    #     check.remove(int(ack))
                    # ack = int(ack)
                        t2 = time.time()
                        RTT = (t2-t1)
                        mylist.append(RTT)

                        print("check",check)
                        sent.append(i)

            except socket.timeout as err:
                print ('caught a timeout')

print ("sequence sent: ", sent)

print ("Delay per packet are: ", mylist)

f.close()
sock.close()
