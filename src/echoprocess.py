from abstractprocess import AbstractProcess, Message


class EchoProcess(AbstractProcess):
    """
    Example implementation of a distributed process.
    This example sends and echo's 10 messages to another process.
    Only the algorithm() function needs to be implemented.
    The function send_message(message, to) can be used to send asynchronous messages to other processes.
    The variables first_cycle and num_echo are examples of variables custom to the EchoProcess algorithm.
    """
    first_cycle = True
    num_echo = 3
    counter = 1
    

    async def algorithm(self):
        # Only run in the beginning
        if self.first_cycle:
            # Compose message
            msg = Message("Hello world", self.idx, "MSG", self.counter)
            # Get first address we can find
            to = list(self.addresses.keys())[0]
            # Send message
            await self.send_message(msg, to)
            self.first_cycle = False
        
        # TODO: 
        # - Get a list of messages from the buffer
        # - Only do self.buffer.get() when the conditions of leaving the buffer holds according to the exercise
        # - Implement the else part of the if statement (probably can delete all of it)
        # - Remove the echo messaging stuff
        print("Buffer size: "+self.buffer.size())
        print(self.buffer.get_queue)
        
        # If we have a new message
        if self.buffer.has_messages():
            
            # Retrieve message
            msg: Message = self.buffer.get()
            print(f'[{self.num_echo}] Got message "{msg.content}" of message type "{msg.type}" from process {msg.sender}, counter: {msg.counter}')
            # Compose echo message
            echo_msg = Message(msg.content, self.idx, msg.type, self.counter)
            self.counter += 1
            # Send echo message
            if msg.type == "MSG":
                # Broadcast Ack to all peers
                for pid in list(self.addresses):
                    ack_msg = Message("[Ack]: "+msg.content, self.idx, "ACK",self.counter)
                    await self.send_message(ack_msg, pid)
            # else:
            #     # Ack received
            #     print("")
            # print(self.buffer)
            await self.send_message(echo_msg, msg.sender)
            self.num_echo -= 1
            if self.num_echo == 0:
                print('Exiting algorithm')
                self.running = False
