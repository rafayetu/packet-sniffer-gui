from .converter import *


class UDP(object):
    """docstring for UDP"""

    def __init__(self, bytes_data):
        super(UDP, self).__init__()
        self.src_port, self.dest_port, self.size = unpack('!HH2xH', bytes_data[:8])
        self.data = bytes_data[8:]
        self.msg_format = (self.src_port, self.dest_port, self.size)


class TCP(object):
    """docstring for TCP"""

    def __init__(self, bytes_data):
        super(TCP, self).__init__()
        (self.src_port, self.dest_port, self.sequence, self.acknowledgment, orf, self.window_size, self.checksum,
         self.urgent_pointer) = unpack('!HHLLHHHH', bytes_data[:20])  # orf= offset_reserved_flags
        offset = (orf >> 12) * 4
        self.flag_non = (orf & 256) >> 8
        self.flag_cwr = (orf & 128) >> 7
        self.flag_ecn = (orf & 64) >> 6
        self.flag_urg = (orf & 32) >> 5
        self.flag_ack = (orf & 16) >> 4
        self.flag_psh = (orf & 8) >> 3
        self.flag_rst = (orf & 4) >> 2
        self.flag_syn = (orf & 2) >> 1
        self.flag_fin = orf & 1
        self.data = bytes_data[offset:]
        self.flags = flagstr(orf, -9, 0)
        self.msg_format = (
        self.src_port, self.dest_port, hex(self.sequence), hex(self.acknowledgment), offset, self.flags,
        self.flag_non, flag(self.flag_non), self.flag_cwr, flag(self.flag_cwr),
        self.flag_ecn, flag(self.flag_ecn), self.flag_urg, flag(self.flag_urg),
        self.flag_ack, flag(self.flag_ack), self.flag_psh, flag(self.flag_psh),
        self.flag_rst, flag(self.flag_rst), self.flag_syn, flag(self.flag_syn),
        self.flag_fin, flag(self.flag_fin),
        self.window_size, hex(self.checksum), self.urgent_pointer)


class ICMP(object):
    """docstring for ICMP"""

    def __init__(self, bytes_data):
        super(ICMP, self).__init__()
        self.type, self.code, self.checksum = unpack('!BBH', bytes_data[:4])
        self.data = bytes_data[4:]

        self.msg_format = (self.type, self.code, hex(self.checksum))
