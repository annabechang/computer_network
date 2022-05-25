import socket
import time
import sys
import os
import math



BUFFER_SIZE = 1000
FILENAME = "message.txt"
WINDOW_SIZE = 5
PKT_SIZE = 1000
NUM_PKTS = int(os.path.getsize(FILENAME)/PKT_SIZE)+1

SEND_TIME = [0]*(NUM_PKTS+1)
RECV_TIME = [0]*(NUM_PKTS+1)
TRANSFERRED_BYTES = [0]*(NUM_PKTS+1)
PER_PKT_RTT = [0]*(NUM_PKTS+1)
PER_PKT_THROUGHPUT = [0]*(NUM_PKTS+1)

ACKNOWLEDGED_SEQUENCES = [0]*(NUM_PKTS+1)
NUM_ACKNOWLEDGEMENTS = [0]*(NUM_PKTS+1)


UDP_IP = ""
UDP_PORT = int(input("Enter the Port number on which your RECV_TIMEeiver is running: "))
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect((UDP_IP,UDP_PORT))

print("Sender is ready to send the file %s" % FILENAME)
print("Number of Packets to send:", NUM_PKTS)




SENT = [0]*(NUM_PKTS+1)
RECEIVED = [0]*(NUM_PKTS+1)
lost=0
WND_START, WND_END = 1, 6




def generate_packets():
	global FILENAME;
	global BUFFER_SIZE;
	global NUM_PKTS;

	f = open(FILENAME, "r")
	message_packets = ["0"]

	for i in range(1, NUM_PKTS+1):
		file_message = f.read(BUFFER_SIZE)
		message_packets.append(file_message)

	f.close()
	return message_packets

def send_packet(seq, data, retransmission_flag):
	global SENT;
	global TRANSFERRED_BYTES;
	global SEND_TIME;

	l = []
	l.append(str(seq)+str("|"))
	l.append(data)

	data = ''.join(l)
	TRANSFERRED_BYTES[seq]=len(str.encode(data))

	if retransmission_flag == 0:
		t1 = time.time()
		if SEND_TIME[seq] == 0:
			SEND_TIME[seq] = t1

	if(sock.send(data.encode())):
		SENT[seq] = 1
		print("Sequence Number of Packet Sent: ",seq)


def receive_acknowledgements(sockt,window_start):
	global NUM_ACKNOWLEDGEMENTS;
	global ACKNOWLEDGED_SEQUENCES;
	global PER_PKT_RTT;
	global BUFFER_SIZE;

	consecutive_receive_timeouts = 3
	current_timeouts = 0

	while current_timeouts < consecutive_receive_timeouts:
		try:
			sockt.setblocking(0)
			sockt.settimeout(0.05)
			ack = sockt.recv(BUFFER_SIZE)
			print("Acknowledgement Received:", int(ack))
			NUM_ACKNOWLEDGEMENTS[int(ack)] += 1
			ACKNOWLEDGED_SEQUENCES[int(ack)] = 1
			for i in range(window_start,int(ack)):
				if PER_PKT_RTT[i] == 0:
					compute_metrics(int(ack),i)
		except socket.timeout as err:
			current_timeouts += 1

def compute_metrics(ack,unack_seq):
	global SEND_TIME;
	global RECV_TIME;
	global PER_PKT_RTT;
	global PER_PKT_THROUGHPUT;
	global TRANSFERRED_BYTES;

	t2 = time.time()
	RECV_TIME[(unack_seq)] = t2
	# print(t2)
	# print(SEND_TIME[j])
	val = float(t2) - float(SEND_TIME[unack_seq])
	# print(val)
	# print(PER_PKT_RTT[j])
	PER_PKT_RTT[(unack_seq)] = (val)


	PER_PKT_THROUGHPUT[(unack_seq)] = TRANSFERRED_BYTES[(unack_seq)]*8/PER_PKT_RTT[unack_seq]

	print("PER_PKT_RTT RECV_TIMEorded")

PACKETS = generate_packets()


#
while WND_START < NUM_PKTS+1:
	for curr_seq in range(WND_START, WND_END):
		print("Current Window: ", range(WND_START, WND_END))
		if SENT[curr_seq] == 0:
			send_packet(curr_seq, PACKETS[curr_seq], 0)
			print("sent seq",curr_seq)
		if curr_seq != WND_END -1:
			continue

		print("outside for loop")

		for curr_seq in range(WND_START, WND_END):
			print("for curr_seq in range(WND_START, WND_END)",WND_START, WND_END)
			receive_time = time.time()

			if receive_time < (SEND_TIME[curr_seq] + 5):

				if ACKNOWLEDGED_SEQUENCES[curr_seq] == 0:
					receive_acknowledgements(sock,WND_START)
					print("ACKNOWLEDGED_SEQUENCES[curr_seq] == 0",sock,WND_START)



					window_shift_count = 0
					for i in range(WND_START, WND_END):
						if ACKNOWLEDGED_SEQUENCES[i] == 1:
							window_shift_count += 1
						else:
							break
					print("WND_START ",WND_START)
					WND_START = WND_START + window_shift_count
					print("WND_END ",WND_END )
					print("WND_START ",WND_START)
					curr_seq = WND_END
					WND_END = WND_END + window_shift_count
					print("WND_END ",WND_END )

					if WND_END>NUM_PKTS+1:

						WND_END = NUM_PKTS+1

					break
			else:
				send_packet(curr_seq, PACKETS[curr_seq], 1)
				lost+=1

		print("window",WND_START,WND_END)

TRANSFERRED_BYTES = [(float(x)) for x in TRANSFERRED_BYTES]
PER_PKT_RTT = [(float(x)) for x in PER_PKT_RTT]
PER_PKT_THROUGHPUT= [(float(x)) for x in PER_PKT_THROUGHPUT]
# print(TRANSFERRED_BYTES)
# print(PER_PKT_RTT)
# print("PER_PKT_THROUGHPUT",PER_PKT_THROUGHPUT)


avg_thu = sum(PER_PKT_THROUGHPUT)/len(PER_PKT_THROUGHPUT)

# avg_thu = sum(TRANSFERRED_BYTES)*8/sum(PER_PKT_RTT)
avg_del = (sum(PER_PKT_RTT)/len(PER_PKT_RTT))*1000
# print(TRANSFERRED_BYTES)
# print("SEND_TIME",SEND_TIME)
# print("RECV_TIME",RECV_TIME)
#
# print("PER_PKT_RTT",PER_PKT_RTT)


print ("average throughput: ", avg_thu," bits per second")
print ("average delay: ", avg_del," milliseconds")
print ("Performance : ", math.log(avg_thu,10)-math.log(avg_del,10))

# f.close()

sock.close()
