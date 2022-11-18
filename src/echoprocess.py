from abstractprocess import AbstractProcess, Message
from colorama import init, Fore, Style
import random

class EchoProcess(AbstractProcess):
    """
    Example implementation of a distributed process.
    This example sends and echo's 10 messages to another process.
    Only the algorithm() function needs to be implemented.
    The function send_message(message, to) can be used to send asynchronous messages to other processes.
    The variables first_cycle and num_echo are examples of variables custom to the EchoProcess algorithm.
    """
    can_send_message = True
    num_echo = 3
    counter = 1
    sent_ack = set()
    sent_msgs_not_delivered = set()
    sent_msgs_not_delivered_ids = set()
    delivered_msgs = set()
    delivered_msg_ids = set()
    
    # used to init printing colors
    init(convert=True)

    # TODO: 
    # - Implement scalar clocks and process ids as tie breakers (wtf does that mean?)
    # - Implement second delivering condition
    # - Implement continuous sending of messages
    # - Make test cases?
    # - Does first delivering condition hold? Lecture says so, although Algorithm 3.18 does not mention it
    # - Order msg queue according to timestamp (self.counter == timestamp?)

    async def algorithm(self):
        # Only run in the beginning
        if self.can_send_message:
            # broadcast a message
            random_message_id = random.randint(1, 99999)
            msg = Message(random_message_id, "BROADCAST Hello world", self.idx, "MSG", self.counter)
            print("Number of peers: "+str(len(self.addresses.keys())))
            for i in range(len(self.addresses.keys())):
                to = list(self.addresses.keys())[i]
                await self.send_message(msg, to)
                print(Fore.BLUE + f'[!] Sent [{msg.type}] "{msg.content}" to process {to}. ID: {msg.message_id}, counter: {msg.counter}')
                # Send everyone ACK of sent message
                self_ack_msg = Message(msg.message_id, msg.content, self.idx, "ACK", self.counter)
                await self.send_message(self_ack_msg, to)
                print(Fore.LIGHTCYAN_EX + f'[!] Sent [{self_ack_msg.type}] "{self_ack_msg.content}" of message ID "{self_ack_msg.message_id}" to process {to}, counter: {self_ack_msg.counter}')
            # Adding msg to set of sent messages
            own_msg = Message(msg.message_id, msg.content, self.idx, "MSG", self.counter)
            self.sent_msgs_not_delivered.add(own_msg)
            self.sent_msgs_not_delivered_ids.add(own_msg.message_id)
            # Adding acknowledgement msg to own queue
            own_ack = Message(msg.message_id, msg.content, self.idx, "ACK", self.counter)
            self.buffer.put(own_ack)
            self.can_send_message = False
        
        # If we have a new message
        if self.buffer.has_messages():

            #  printing buffer messages
            print(Fore.YELLOW + "------------ "+str(self.buffer.size())+" BUFFER MESSAGES: --------------")
            for i in range(self.buffer.size()):
                buf_msg: Message = self.buffer.queue_value(i)
                print(Fore.YELLOW + f'[!] Got [{buf_msg.type}]: "{buf_msg.content}" from process {buf_msg.sender}. ID: {buf_msg.message_id}, counter: {buf_msg.counter}')
            print(Fore.YELLOW + "-------------- END OF BUFFER -----------------")

            # Go through buffered messages (inefficient, I know)
            for i in range(self.buffer.size()):
                buf_msg: Message = self.buffer.queue_value(i)
                # Check if there are MSGs in buffer for which no ACK has been sent
                if (buf_msg.type == "MSG") and (buf_msg.message_id not in self.sent_ack):
                    # Broadcast Ack to all peers
                    for i in range(len(self.addresses.keys())):
                        ack_msg = Message(buf_msg.message_id, buf_msg.content, self.idx, "ACK", self.counter)
                        to = list(self.addresses.keys())[i]
                        await self.send_message(ack_msg, to)
                        # Add message ID of received message to set of sent acknowledgements
                        self.sent_ack.add(buf_msg.message_id)
                        print(Fore.LIGHTCYAN_EX + f'[!] Sent [{ack_msg.type}] "{ack_msg.content}" of message ID "{ack_msg.message_id}" to process {to}, counter: {ack_msg.counter}')
            
                    
                found_first_msg = False
                # Search for acknowledgements of message in queue
                if (buf_msg.type == "MSG") and (found_first_msg == False):
                    found_first_msg = True
                    ack_index_counter = 0
                    for i in range(self.buffer.size()):
                        buf_ack_msg: Message = self.buffer.queue_value(i)
                        if buf_ack_msg.type == "ACK" and buf_msg.message_id == buf_ack_msg.message_id:
                            a = 1
                        ack_index_counter += 1

            head_of_queue: Message = self.buffer.queue_value(0)
            # if head_of_queue.type == "ACK" and 
            # if head_of_queue.message_id in self.delivered_msg_ids:
            #     self.buffer.get()

            # Remove from buffer list and deliver condition 1: Message at head of queue (oldest message the process knows about)
            if head_of_queue.type == "MSG":
                print(Fore.GREEN + f'[!] DELIVERED [{head_of_queue.type}] "{head_of_queue.content}" of message ID "{head_of_queue.message_id}", counter: {head_of_queue.counter}')
                self.delivered_msgs.add(head_of_queue)
                self.delivered_msg_ids.add(head_of_queue.message_id)
                self.buffer.get()
            # Remove from buffer list and deliver condition 2: Process received ACK from all processes (no older message will arrive)
            # TODO: Implement


        self.counter += 1
        self.num_echo -= 1
        if self.num_echo == 0:
            print('Exiting algorithm')
            self.running = False
