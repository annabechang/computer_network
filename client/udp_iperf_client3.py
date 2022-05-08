import socket
import select
import time
import random

# UDP_IP = ""

UDP_IP = "173.230.149.18"
IN_PORT = int(input("enter port:"))
timeout = 1
count = 0
sleep_t = (timeout * 2 ** count +
                 random.uniform(0, 1))

buf=4068
tar_size = 1300000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.bind((UDP_IP, IN_PORT))

data = "ping"
sock.sendto(data.encode('ascii'), (UDP_IP, IN_PORT))

data, addr = sock.recvfrom(4068)
# file_name = data.strip()
# print ("File name:", file_name)
t1 = time.perf_counter_ns()
f = open("test.txt", 'wb')

# try:
while(f.tell()<tar_size):
    print("received %: ", round(f.tell()/tar_size*100))
    # t1 = time.perf_counter_ns()


    ready = select.select([sock], [], [], timeout)
    print("ready",ready)
    if ready[0]:
        f.write(data)

        data, addr = sock.recvfrom(4068)
    # else:
    #     print ("%s Finish!" % file_name)
        # sock.settimeout(timeout)
        # data,addr = sock.recvfrom(buf)
        t2 = time.perf_counter_ns()
        time_delta = t2 - t1
        throughput = (f.tell()) / time_delta
        print("f.tail",f.tell(), "tar size",tar_size)
        # print(time_delta,throughput)
    else:
        print("break")
        break


print(f"Time elapsed: {time_delta} ms" )
print(f"Throughput: {throughput} bps")
print('Size of file is', f.tell(), 'bytes')

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
