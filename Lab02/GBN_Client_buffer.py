import sys, time, argparse
import socket
from util_new import *
from scapy.all import raw

RECV_BUFFER_SIZE = 2048

# Get the server hostname and port as command line arguments
def get_args(argv):
    parser = argparse.ArgumentParser(description="UDP File Transfer Client using Go-Back-N protocol")
    parser.add_argument('-p', '--port', required=False, default=12000, type=int)
    parser.add_argument('-a', '--address', required=True)
    parser.add_argument('-f', '--filename', required=False, default="test_file.txt") 
    parser.add_argument('-w', '--window-size', required=False, default=5, type=int) #default is 1
    parser.add_argument('-b', '--packet-size', required=False, default=1000, type=int)
    parser.add_argument('-t', '--timeout-interval', required=False,
                        default=1.0, type=float, help='timeout interval in seconds')
    return parser.parse_args()

def main(argv):
    # Parse command line args
    args = get_args(argv)

    # Initialize
    packet_size = args.packet_size
    timeout = args.timeout_interval
    window_size = args.window_size
    window = []
    bytes_sent = 0
    seq = 0
    buffered_packets = {} 

    # Open file to read from
    infile = open(args.filename, 'rb')

    # Create client socket (note use of SOCK_DGRAM for UDP) 
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(timeout)

     # new add Send filename packet
    filename = args.filename.encode()
    filename_pkt_header = PacketHeader(type=PacketHeader.TYPE_FILENAME, seq_num=seq, length=len(args.filename))
    filename_pkt=filename_pkt_header / filename
    client_socket.sendto(bytes(filename_pkt), (args.address, args.port))
    print(f"Send:Filename_PacketHeader: type={PacketHeader.TYPE_FILENAME}, seq_num={seq}, length={len(args.filename)}, filename={args.filename}")
    seq += 1
    
    # Send file data packet
    start_time = time.time()
    data = infile.read(packet_size)
    sent_end_pkt = False
    
    while True:
        # We still have data to send and currently have space in our window to send it
        while data and len(window) < window_size:
            # package and send data
            pkt_header = PacketHeader(type=PacketHeader.TYPE_DATA, seq_num=seq, length=len(data))
            pkt = raw(pkt_header) + data
            window.append((seq,pkt))
            buffered_packets[seq] = pkt  # new add:Store the packet in the buffer
            client_socket.sendto(pkt, (args.address, args.port))
            print(f"Send:PacketHeader: type={PacketHeader.TYPE_DATA}, seq_num={seq}, length={len(data)}")
            seq += 1
            bytes_sent += len(data)
            data = infile.read(packet_size)

        # Special case for termination signal. We have sent all the file data,
        # now send TYPE_END packet to let the receiver know we are done
        if not data and not sent_end_pkt and len(window) < window_size:
            pkt_header = PacketHeader(type=PacketHeader.TYPE_END, seq_num=seq, length=0)
            pkt = raw(pkt_header)
            window.append((seq,pkt))
            buffered_packets[seq] = pkt
            client_socket.sendto(pkt, (args.address, args.port))
            print(f"Send: PacketHeader: type={PacketHeader.TYPE_END}, seq_num={seq}, length=0")
            sent_end_pkt = True

        # Wait for response or timeout
        try:
            pkt, address = client_socket.recvfrom(RECV_BUFFER_SIZE)
            recv_header = PacketHeader(pkt[:PacketHeader.header_len])
            ack = recv_header.seq_num
            print(f"Received ACK: seq={ack}")
            
            # Check if the filename packet is acknowledged
            if ack == 0:
                print("Filename packet acknowledged by server.")
            
            # advance window (if possible)
            while len(window) > 0:
                first_seq, first_pkt = window[0]
                #h = PacketHeader(pkt[:PacketHeader.header_len])
                if first_seq <= ack:
                    window.pop(0)
                    del buffered_packets[first_seq]
                    print(f"{first_seq} ACK received,removing from window ")
                else:
                    break

            # If we are done sending data, check whether receiver has now
            # acknowledged everything we sent. If so, we are done and can quit!
            if sent_end_pkt and len(window) == 0:
                print("Final packet with seq {} acknowledged. Time to quit...".format(seq))
                break

        except socket.timeout as e:
            ## Timeout occured ##
            if len(window) > 0:
                earliest_seq = min(buffered_packets.keys())  # Find the earliest unacknowledged packet
                client_socket.sendto(buffered_packets[earliest_seq], (args.address, args.port))
                print(f"Timeout:Retransmitting only the earliest unackowledged packet {earliest_seq}")
            else:
                print(f"TIMEOUT: No unacknowledged packets to resend.")
            client_socket.settimeout(timeout)
        
    # Close the client socket and file
    client_socket.close()
    infile.close()

    # Print stats
    end_time = time.time()
    elapsed_time = end_time - start_time
    throughput = (bytes_sent * 8) / (elapsed_time)
    print("\n=== Final Stats ===")
    print("Bytes transferred: {}".format(bytes_sent))
    print("Time Elapsed: {} sec".format(elapsed_time))
    print("Throughput: {} Mbps".format(throughput/1000000.0))

if __name__ == "__main__":
    main(sys.argv[1:])
