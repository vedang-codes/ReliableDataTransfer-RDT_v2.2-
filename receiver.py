class ReceiverProcess:
    """ Represent the receiver process in the application layer  """
    __buffer = list()

    @staticmethod
    def deliver_data(data):
        """ deliver data from the transport layer RDT receiver to the application layer
        :param data: a character received by the RDT RDT receiver
        :return: no return value
        """
        ReceiverProcess.__buffer.append(data)

    @staticmethod
    def get_buffer():
        """ To get the message the process received over the network
        :return:  a python list of characters represent the incoming message
        """
        return ReceiverProcess.__buffer


class RDTReceiver:
    """" Implement the Reliable Data Transfer Protocol V2.2 Receiver Side """

    def __init__(self):
        self.sequence = '0'

    @staticmethod
    def is_corrupted(packet):
        """ Check if the received packet from sender is corrupted or not
            :param packet: a python dictionary represent a packet received from the sender
            :return: True -> if the reply is corrupted | False ->  if the reply is NOT corrupted
        """
        return packet['checksum'] != RDTReceiver.get_checksum(packet['data'])

    @staticmethod
    def is_expected_seq(rcv_pkt, exp_seq):
        """ Check if the received reply from receiver has the expected sequence number
         :param rcv_pkt: a python dictionary represent a packet received by the receiver
         :param exp_seq: the receiver expected sequence number '0' or '1' represented as a character
         :return: True -> if ack in the reply match the   expected sequence number otherwise False
        """
        return rcv_pkt['sequence_number'] == exp_seq

    @staticmethod
    def make_reply_pkt(seq, checksum):
        """ Create a reply (feedback) packet with to acknowledge the received packet
        :param seq: the sequence number '0' or '1' to be acknowledged
        :param checksum: the checksum of the ack the receiver will send to the sender
        :return:  a python dictionary represent a reply (acknowledgement)  packet
        """
        reply_pkt = {
            'ack': seq,
            'checksum': checksum
        }
        return reply_pkt

    def rdt_rcv(self, rcv_pkt):
        """  Implement the RDT v2.2 for the receiver
        :param rcv_pkt: a packet delivered by the network layer 'udt_send()' to the receiver
        :return: the reply packet
        """

        if not RDTReceiver.is_corrupted(rcv_pkt) and RDTReceiver.is_expected_seq(rcv_pkt, self.sequence):
            # If the received packet is not corrupted and has the expected sequence number
            data = rcv_pkt['data']
            ReceiverProcess.deliver_data(data)
            reply_pkt = RDTReceiver.make_reply_pkt(self.sequence, RDTReceiver.get_checksum(data))
            self.sequence = '0' if self.sequence == '1' else '1'  # Toggle the sequence number
            return reply_pkt

        # If the received packet is corrupted or has an unexpected sequence number, return None
        return None
