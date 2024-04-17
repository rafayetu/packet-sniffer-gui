import socket
from .protocols.data_link import *
from .protocols.network import *
from .protocols.transport import *
from .messages import MessageBox
import platform, time
from threading import Thread

valid_protocols = ['TCP', 'UDP', 'ICMP']
system_platform = platform.system()


class PacketSniffer(object):
    def __init__(self):
        super(PacketSniffer, self).__init__()
        if system_platform == "Windows":
            self.HOST = socket.gethostbyname(socket.gethostname())
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_RAW)
            self.conn.bind(('localhost', 0))
            self.conn.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
        else:
            self.conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
        self.buff_size = 65535  # 2^16=65536
        self.msg = MessageBox()

    def capture_packets(self, treeview, update_packet, packet_no):
        start_time = time.time()
        packets = {}
        self.msg.basic_info()

        while True:
            bytes_data, addr = self.conn.recvfrom(self.buff_size)
            packet = Packet(bytes_data, packet_no, self.msg)
            packets[packet_no] = packet
            if system_platform == "Windows" or packet.ethernet.proto_title == 'EGP':
                data = packet.treeview_data(start_time=start_time)
                th = Thread(target=treeview, args=(data[0], data[1],))
                th.start()
                update_packet(packet_no, packet)
                packet_no += 1


class Packet(object):
    """docstring for Packet"""

    def __init__(self, bytes_data, packet_no, msg):
        super(Packet, self).__init__()
        self.bytes_data = bytes_data
        self.packet_no = packet_no
        self.msg = msg
        self.capture_time = time.time()
        if system_platform != "Windows":
            self.ethernet = Ethernet(bytes_data)
        if system_platform == "Windows" or self.ethernet.proto_title == 'EGP':
            self.ip = IPv4(self.bytes_data) if system_platform == "Windows" else IPv4(self.ethernet.data)

            self.msg.basic_info(
                (self.packet_no, self.ip.proto_title, self.ip.src_ip, self.ip.target_ip, len(self.ip.data)))
            if self.ip.proto_title in valid_protocols:
                self.transport = self.get_transport(self.ip)

    def treeview_data(self, start_time):
        return (self.packet_no, [self.capture_time - start_time, self.ip.src_ip, self.ip.target_ip, self.ip.proto_title,
                                 len(self.ip.data)])

    def get_transport(self, ip):
        if ip.proto_title == 'TCP':
            transport = TCP(ip.data)
        elif ip.proto_title == 'UDP':
            transport = UDP(ip.data)
        elif ip.proto_title == 'ICMP':
            transport = ICMP(ip.data)
        return transport

    def get_packet_info(self):
        packet_header = self.msg.headers['Packet'].format(self.packet_no)
        ethernet_msg = self.msg.headers['ETH'] % self.ethernet.msg_format if system_platform != "Windows" else ""
        ipv4_msg = self.msg.headers['IPv4'] % self.ip.msg_format

        if self.ip.proto_title in valid_protocols:
            transport_msg = self.msg.headers[self.ip.proto_title] % self.transport.msg_format
            msg = packet_header + ethernet_msg + ipv4_msg + transport_msg
        else:
            msg = packet_header + ethernet_msg
        print(msg)
        return msg
