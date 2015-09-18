# -*- coding: utf-8 -*-
import pika


class BaseWorker(object):
    """The base worker is the class that all 'worker' nodes derive from."""
    def __init__(self, hostname, name=''):
        """It instantiates three queues: tasking, results, and errors.  The naming for these queues is based upon the class
        name of the workers that derive from it.

        :param hostname: Indicates the hostname of the RabbitMQ server to connect to
        :param name: Indicates the name of the queue or worker.  Can be left blank and it will derive from the class name
        """
        self._name = name if name != '' else self.__class__.__name__
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname))
        self.tasking_channel = self.connection.channel()
        self.tasking_channel.queue_declare(queue='{}_tasking'.format(self._name), durable=True)
        self.results_channel = self.connection.channel()
        self.results_channel.queue_declare(queue='{}_results'.format(self._name), durable=True)
        self.error_channel = self.connection.channel()
        self.error_channel.queue_declare(queue='{}_errors'.format(self._name), durable=True)

    def callback(self, ch, method, properties, body):
        """
        :param ch: You should not need to modify this field
        :param method: This references the function that your worker will process
        :param properties: You should not need to modify this field
        :param body: This is the message being passed to and from the queues
        """
        pass

    def run(self):
        pass
