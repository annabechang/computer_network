# import socket
# import os
#
# # needed data in the input file
# '''
#  IP address of server.
#  Well-known port number of server.
#  Port number of client.
#  Filename to be transferred (should be a large file).
#  Initial receiving sliding-window size (in datagram units).
# '''
# # reading client input file
#
# server_IP = '127.0.0.1'
# server_port = 12001
# client_port = 12001
# requested_file = "client_input.txt"
#
#
# received_file = open(requested_file, "wb")
#
# def request_file_from_server():
#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     sock.bind(('', client_port))
#     sock.settimeout(10)
#     sock.sendto(requested_file.encode(), (server_IP, server_port))  # request new file
#     sock.settimeout(None)
#     return sock
import socket
import time
import sys

if len(sys.argv) > 1:
    maxSendRateBytesPerSecond = int(sys.argv[1])*128
if len(sys.argv) > 2:
    maxSendRateBytesPerSecond = int(sys.argv[1])*128
    run_time = int(sys.argv[2])
else:
    maxSendRateBytesPerSecond = (100*1472)
    run_time = 5
#Hard stop the app if it attempts to send traffic above 100mbit/s
if maxSendRateBytesPerSecond > 99000000:
    sys.exit("Bandwidth above 99Mbps is not allowed")
#Hard limit maximum running time to 5 minutes.
if run_time > 300:
    run_time = 300

#Total packets to be sent which is used for detecting packet loss.
total_packets = (maxSendRateBytesPerSecond/1472) * run_time

def ConvertSecondsToBytes(numSeconds):
    return numSeconds*maxSendRateBytesPerSecond

def ConvertBytesToSeconds(numBytes):
    return float(numBytes)/maxSendRateBytesPerSecond

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(('', 5005))

# We'll add to this tally as we send() bytes, and subtract from
# at the schedule specified by (maxSendRateBytesPerSecond)
bytesAheadOfSchedule = 0

# Dummy data buffer, just for testing
dataBuf = bytearray(1024)

prevTime = None
t_end = time.time() + run_time
print("Sending %s Kbps for %s seconds (%s packets in total)" % (maxSendRateBytesPerSecond * 8, run_time, int(total_packets)))
while time.time() < t_end:
   now = time.time()
   if (prevTime != None):
      bytesAheadOfSchedule -= ConvertSecondsToBytes(now-prevTime)
   prevTime = now

   numBytesSent = sock.send(dataBuf)
   if (numBytesSent > 0):
      bytesAheadOfSchedule += numBytesSent
      if (bytesAheadOfSchedule > 0):
         time.sleep(ConvertBytesToSeconds(bytesAheadOfSchedule))
   else:
      print ("Error sending data, exiting!")
      break
end_string = b'END!'
sock.send(end_string)
