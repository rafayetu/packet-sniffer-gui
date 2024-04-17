from .converter import *


class Ethernet(object):
    """docstring for Ethernet"""

    def __init__(self, bytes_data):
        super(Ethernet, self).__init__()
        dest, src, prototype = unpack('! 6s 6s H', bytes_data[:14])
        self.dest_mac = get_mac_addr(dest)
        self.src_mac = get_mac_addr(src)
        self.proto = protocol(prototype)
        self.proto_title = get_protocol_title(self.proto)
        self.data = bytes_data[14:]
        self.msg_format = (self.src_mac, self.dest_mac, self.proto)
