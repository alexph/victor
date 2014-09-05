from victor.transport import MemoryTransport
from victor.logger import logger

from Queue import Queue

import msgpack


class Message(object):
    sender = None
    payload = None
    receivers = []

    def set_sender(self, sender):
        self.sender = sender

    def get_sender(self):
        return self.sender

    def set_payload(self, payload):
        self.payload = payload

    def get_payload(self):
        return self.payload

    def add_receiver(self, receiver):
        self.receivers.append(receiver)

    def set_receivers(self, receivers):
        self.receivers = receivers

    def get_receivers(self):
        return self.receivers

    def serialize(self):
        msg = {
            'sender': self.get_sender(),
            'payload': self.get_payload(),
            'receivers': self.get_receivers()
        }

        return msgpack.dumps(msg)

    def deserialize(self, msg):
        msg = msgpack.loads(msg)

        self.set_sender(msg['sender'])
        self.set_payload(msg['payload'])
        self.set_receiver(msg['receivers'])


class BasePipeline(object):
    def __init__(self, wf):
        logger.info('%s starting' % self.__class__.__name__)

        self.wf = wf
        self.queue = Queue()
        self.transport = MemoryTransport(wf, self.queue)

    def start(self, iter_generator):
        raise NotImplementedError()


class LocalPipeline(BasePipeline):
    def start(self, iter_generator):
        for item in iter_generator():
            msg = self._create_msg('root', item)

            self.transport.send(msg)
            self._work()

    def _create_msg(self, sender, payload):
        msg = Message()
        msg.set_sender(sender)
        msg.set_payload(payload)
        msg.set_receivers(self.wf.get_outputs(sender))

        logger.info('%s sends a message => %s' % (
            sender,
            ', '.join(self.wf.get_outputs(sender)))
        )

        logger.debug(payload)

        return msg

    def _transform(self, tf, payload):
        tf.push_data(payload)
        return tf.output

    def _work(self):
        while not self.queue.empty():
            logger.info('Got message on %s loopback' % self.__class__.__name__)
            #
            # Retreive from fake queue
            msg = self.queue.get()

            #
            # The message sender list
            receivers = msg.get_receivers()

            #
            # For each tf in sender list
            for recv in receivers:
                tf = self.wf.get_transformer(recv)
                out = self._transform(tf, msg.get_payload())

                #
                # Create outgoing message
                msg = self._create_msg(recv, out)

                if msg.get_receivers():
                    self.transport.send(msg)
                else:
                    logger.warning('Message was blackholed (nobody wants it)')

            self._work()
