from .converter import *


class IPv4(object):
    """docstring for IPv4"""

    def __init__(self, bytes_data):
        super(IPv4, self).__init__()
        iph = unpack('!BBHHHBBH4s4s', bytes_data[:20])
        version_ihl = iph[0]
        self.type_of_service = iph[1]
        self.total_length = iph[2]
        self.identification = hex(iph[3])
        self.flags = iph[4] >> 13  # binary right shift of 13 bits

        self.flag_res = (self.flags & 4) >> 2
        self.flag_nf = (self.flags & 2) >> 1
        self.flag_mf = self.flags & 1

        self.flagstr = "%s%s%s" % (self.flag_res, self.flag_nf, self.flag_mf)
        self.fragment = iph[4] & 8191  # 8191 = 1111111111111 [bitwise and for 13bits]
        self.version = version_ihl >> 4
        self.header_length = (version_ihl & 0xF) * 4
        self.ttl = iph[5]
        self.proto = iph[6]
        self.proto_title = get_protocol_title(self.proto)
        self.checksum = hex(iph[7])
        self.src_ip = get_ipv4(iph[8])
        self.target_ip = get_ipv4(iph[9])
        self.data = bytes_data[self.header_length:]

        self.msg_format = (self.version, self.header_length, self.type_of_service, self.total_length,
                           self.identification, self.flagstr, self.flag_res, flag(self.flag_res),
                           self.flag_nf, flag(self.flag_nf), self.flag_mf, flag(self.flag_mf),
                           self.fragment, self.ttl, "{}--> ({})".format(self.proto_title, self.proto),
                           self.checksum, self.src_ip, self.target_ip)
