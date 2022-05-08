import socket
import time
import sys
import os

UDP_IP = ""
# UDP_PORT = 12001
# UDP_IP = ""
UDP_PORT = 5005
buf = 1000
file_name = "test.txt"
n_packet = 5

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.bind(('', UDP_PORT))
sock.connect((UDP_IP,UDP_PORT))


print("server is ready to send file %s" % file_name)

print ("Sending Total number of packet %s ..." % str(n_packet).encode())
sock.send(str(n_packet).encode())
check = list(range(1,int(n_packet)+1))
print("check list",check)
mylist=[]
sent = []
f = open(file_name, "r")

data = f.read(buf)

while (len(check)!=0):
    # for i in range(1,n_packet+1):
    for i in check:
        print("processing seq",i)
        l = []
        #append sequence number
        l.append(str("Sequence Number: ")+str(i)+str("\r\n"))
        l.append(data)

        data = ''.join(l)
        #
        print("data header: ", data[:20])
        # print("sending data of sequence number: ",data[0])
        print("size of the data sent:",len(data))
#         # while(data):.
        t1 = time.time()
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
                    t2 = time.time()
                    RTT = (t2-t1)
                    mylist.append(RTT)

                    # if int(ack) in check:
                    #     check.remove(int(ack))
                    # ack = int(ack)
                    check.remove(int(i))
                    print("check",check)
                    sent.append(i)
            except socket.timeout as err:
                print ('caught a timeout')

print ("sequence sent: ", sent)

print ("Stored RTTs are: ", mylist)
#                     # print ('print retry')
#                     #
#                     # ack, clientAddress = sock.recvfrom(buf)
#                     # print("acknowledgement received:",int(ack),"from",str(clientAddress))
#                     #
                # if int(ack) in check:
                #     check.remove(int(ack))
                # ack = int(ack)
                # continue
#
#
#                     i+=1
#
#                     eof = "END"
#                     print("check list",check)
#
#
#
#
#                     sock.sendto(eof.encode(), (UDP_IP,UDP_PORT))
#
#
# f.close()
# sock.close()
