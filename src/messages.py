import sys

choice_options = {
    "PrimaryChoice": [1],
    "SecondChoice": [1, 0],
    "ThirdChoice": [1, 2, 3, 0],
}

message_list = {
    "PrimaryChoice": """
	1. Capture packets and analyze it
Press: """,

    "SecondChoice": """
	1. Print details of packets
	0. Exit
Press: """,

    "ThirdChoice": """
	1. Print details of all packets
	2. Print details of a specific packet
	3. Print details of all packets in range
	0. Exit from option '1'
Press: """,

    "FileName": """
	Enter a file name(Note: File will be saved in ".pcap" format): """,

    "PacketNumber": """
	Enter the number of packets you want to capture: """,

    "InvalidMessage": "Invalid Choice Message '{}'",

    "InalidChoice": """-->Please Enter Valid Option<--
	Press: """,

    "InalidNumber": """-->Please Enter Valid Number<--
	Press: """,

    "Range": """
	Enter packet number range: """,

    "Packet": """
	Enter packet number:  """,

}

headers = {
    "Packet": """
======================================================

                 Packet NO : {}
*****************************************************

	""",

    "ETH": """
Ethenet Header :
	-->Source Ethernet Address        : %s
	-->Destination Ethernet Address   : %s
	-->Ethernet Type                  : %s

	""",

    "IPv4": """
IP Header:
	-->Version                        : %s
	-->Header Length                  : %s
	-->Type of service                : %s
	-->Total Length                   : %s
	-->Identification                 : %s
	-->Flags                          : %s
		%s.. = Reserved: %s
		.%s. = DF: %s
		..%s = MF: %s

	-->Fragment                       : %s
	-->TTL                            : %s
	-->Protocol                       : %s
	-->Header Checksum                : %s
	-->Source IP                      : %s
	-->Destination IP                 : %s

	""",

    "TCP": """
TCP Header:
	-->Source Port                    : %s
	-->Destinaton Port                : %s
	-->Sequence Number                : %s
	-->Acknowledgement Number         : %s
	-->Header Length                  : %s
	-->Flags                          : %s

		000. .... .... = Reserved: 
		...%s .... .... = Nonce: %s
		.... %s... .... = Congestion Window Reduced (CWR): %s
		.... .%s.. .... = ECN-Echo: %s
		.... ..%s. .... = Urgent: %s
		.... ...%s .... = Acknowledgement: %s
		.... .... %s... = Push: %s
		.... .... .%s.. = Reset: %s
		.... .... ..%s. = Syn: %s
		.... .... ...%s = Fin: %s

	-->Window Size Value            : %s
	-->Checksum                     : %s
	-->UrgentPointer                : %s

""",

    "UDP": """
UDP Header:
	-->Source Port                    : %s
	-->Destinaton Port                : %s
	-->Size Value                     : %s
""",

    "ICMP": """
ICMP Header:
	-->Type of message                : %s
	-->Code                           : %s
	-->Checksum                     : %s

""",

}


class MessageBox(object):
    """docstring for MessageBox"""

    def __init__(self):
        super(MessageBox, self).__init__()

        self.message_list = message_list
        self.choice_options = choice_options
        self.headers = headers

    def ask_choice(self, msg):
        choice = self.get_input(msg)
        while True:
            if choice in map(str, self.choice_options[msg]):
                return int(choice)
            else:
                choice = input(self.message_list["InalidChoice"])

    def get_number(self, msg, limit=False):
        choice = self.get_input(msg)
        while True:
            try:
                if (limit and int(choice) <= limit) or not limit:
                    return int(choice)
                else:
                    choice = input(self.message_list["InalidNumber"])
            except:
                choice = input(self.message_list["InalidNumber"])

    def get_range(self, msg, limit=False):
        choice = self.get_input(msg).split(' ')
        while True:
            try:
                choice = map(int, choice)
                if (limit and int(choice[0]) <= limit and int(choice[1]) <= limit) or not limit:
                    return map(int, choice)
                else:
                    choice = input(self.message_list["InalidNumber"])
            except:
                choice = input(self.message_list["InalidNumber"])

    def get_input(self, msg):
        if msg in self.message_list:
            return input(self.message_list[msg])
        else:
            print(self.message_list["InvalidMessage"].format(msg))
            sys.exit()

    def basic_info(self, data=[]):
        headers = ('Packet No', 'Protocol', 'Source Address', 'Destination Address', 'Packet Size')
        print(" %-15s %-10s %-25s %-25s %-15s" % (data if len(data) else headers))
