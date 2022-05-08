

import socket
import os
class NewConnection(object):
    def __init__(self, device_type):
        # Start with a default state.
        if device_type == 'server':
            self.state = Waiting_for_call_0()
        elif device_type == 'client':
            self.state = Waiting_for_0_From_below()

    def on_event(self, event):
        # The next state will be the result of the on_event function.
        self.state = self.state.on_event(event)


# write log
protocol_type = "sr"
file_path = "./log_file.txt"
log_file = open(file_path, "w")


def write_log(event):
    log_file = open(file_path, "a")
    log_file.write(event + "\n")
    print(event)
    return 1

# reading input file
server_input_file = open("test.txt", "r")
Input_list = server_input_file.read().splitlines()
server_port = 12001
Max_sending_window_size = 1
random_SeedValue = 0
loss_Probability = 0

# initialize the global variables
chunk_size = 500  # size of each data packet
Header_size = 12  # size of header in bytes
server_ip = '127.0.0.1'

list_of_must_dropped_seq_numbers = []

def waiting_for_new_request():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', server_port))
    write_log("Waiting for client...\n")
    requested_file, client_address = sock.recvfrom(100)
    write_log(str(("Server:   Requested file", requested_file, "from", client_address)))
    return requested_file, client_address

def get_must_dropped_packets(file_name, probability, size_of_packet, seed_value):
    random.seed(seed_value)
    size_of_file = os.path.getsize(file_name)
    print("size of file= ", size_of_file)
    number_of_chunks = int(size_of_file / size_of_packet)
    print("number_of_chunks", number_of_chunks)
    number_of_must_dropped = int(number_of_chunks * probability)
    print("number_of_must_dropped", number_of_must_dropped)
    print("random", random.randint(seed_value, number_of_must_dropped))
    for i in range(number_of_must_dropped):
        list_of_must_dropped_seq_numbers.append(random.randint(0, number_of_chunks))
    return list_of_must_dropped_seq_numbers

def get_decision(list_of_must_dropped_seq_numbers, seq_number):
    if list_of_must_dropped_seq_numbers.__contains__(seq_number):
        return False  # drop it
    else:
        return True  # don't drop it

def print_dropped_seq(list_of_must_dropped_seq_numbers):
    for i in range(len(list_of_must_dropped_seq_numbers)):
        print(list_of_must_dropped_seq_numbers[i])

if Max_sending_window_size > 1:
    print("Stop and wait protocol can't handle more than 1 datagram window size")

elif Max_sending_window_size == 1:
    file, address = waiting_for_new_request()
    requested_file = open(file, "rb")
    server = NewConnection('server')

    # establish a simulation environment
    list_of_dropped = get_must_dropped_packets(file, loss_Probability, chunk_size, random_SeedValue)
    #print_dropped_seq(list_of_dropped)

    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket.bind(('', 54321))

    while 1:
        server.on_event((requested_file, address, list_of_dropped, socket))
