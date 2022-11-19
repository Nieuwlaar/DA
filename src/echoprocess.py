from abstractprocess import AbstractProcess, Message
import random

class EchoProcess(AbstractProcess):
    """
    Example implementation of a distributed process.
    This example sends and echo's 10 messages to another process.
    Only the algorithm() function needs to be implemented.
    The function send_message(message, to) can be used to send asynchronous messages to other processes.
    The variables first_cycle and num_echo are examples of variables custom to the EchoProcess algorithm.
    """
    first_cycle = True
    num_echo = 15
    counter = 1
    messages_awaiting_ack = []

    async def algorithm(self):
        # Only run in the beginning
        if self.first_cycle:
            # Compose message
            random_message_id = random.randint(0, len(self.random_messages)-1)
            #print(self.random_messages)
            random_message = self.random_messages[random_message_id]
            msg = Message(True, random_message, self.idx, self.counter)
            msg_ack = Message(False, random_message, self.idx, self.counter, self.idx, self.counter)
            # Get first address we can find
            for i in range(len(self.addresses.keys())):
                to = list(self.addresses.keys())[i]
            # Send message
                print(f' Sending MSG: {msg} to: {to}')
                await self.send_message(msg, to)
                await self.send_message(msg_ack, to)
            self.messages_awaiting_ack.append([random_message, self.idx, self.counter])
            self.messages_awaiting_ack.append(1)
            print(self.messages_awaiting_ack)
            self.first_cycle = False

        # If we have a new message
        if self.buffer.has_messages():

            #  printing buffer messages
#             print("------------ "+str(self.buffer.size())+" BUFFER MESSAGES: --------------")
#             for i in range(self.buffer.size()):
#                 buf_msg: Message = self.buffer.queue_value(i)
#                 print(f'[!] Got [{buf_msg.is_message}]: "{buf_msg.content}" from process {buf_msg.sender}. counter: {buf_msg.counter}')
#             print("-------------- END OF BUFFER -----------------")
            # Retrieve message
            msg: Message = self.buffer.get()
                
            #print(f'[{self.num_echo}] Got message "{msg.content}" from process {msg.sender}, counter: {msg.counter}')
            if msg.is_message == True:
                print(f'Got message "{msg.content}" from process {msg.sender} with counter: {msg.counter}')
                self.messages_awaiting_ack.append([msg.content, msg.sender, msg.counter])
                self.messages_awaiting_ack.append(1)
                print(self.messages_awaiting_ack)
            else:
                print(f'Got Acknoledgement "{msg.content}" from process {msg.sender} with counter: {msg.counter} origin sender: {msg.origin_sender} origin counter: {msg.origin_counter}')
                try:
                    index = self.messages_awaiting_ack.index([msg.content, msg.origin_sender, msg.origin_counter])
                except:
                    self.messages_awaiting_ack.append([msg.content, msg.origin_sender, msg.origin_counter])
                    self.messages_awaiting_ack.append(1)
                    print(self.messages_awaiting_ack)
                else:
                    self.messages_awaiting_ack[index+1] += 1
                    print(self.messages_awaiting_ack)
            
            if msg.counter > self.counter:
                print(f' Self counter: {self.counter}, message counter: {msg.counter}, msg counter is larger')
            if msg.counter < self.counter:
                print(f' Self counter: {self.counter}, message counter: {msg.counter}, self counter is larger')            
            else:
                print(f' Self counter: {self.counter}, message counter: {msg.counter}, counters are equal')    
            # Compose echo message
            self.counter = max(self.counter, msg.counter)
            self.counter += 1
            print(f' new self counter: {self.counter}')
            if msg.is_message == True:
                ack_msg = Message(False, msg.content, self.idx, self.counter, msg.sender, msg.counter)
                for i in range(len(self.addresses.keys())):
                    to = list(self.addresses.keys())[i]
                # Send echo message
                    print(f' Sending ACK: {msg.content}, from {msg.sender} with counter {msg.counter} to: {to}')
                    await self.send_message(ack_msg, to)
            
            if m
            
            self.num_echo -= 1
            if self.num_echo == 0:
                print('Exiting algorithm')
                self.running = False
