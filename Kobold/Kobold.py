# -*- coding: utf-8 -*-
import pika


class BaseWorker(object):
    """The base worker is the class that all 'worker' nodes derive from.
    It has no properties or methods and can easily be extended to serve many purposes.
    """
    def __init__(self, hostname, name=''):
        self._name = name if name != '' else self.__class__.__name__
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname))
        self.tasking_channel = self.connection.channel()
        self.tasking_channel.queue_declare(queue='{}_tasking'.format(self._name), durable=True)
        self.results_channel = self.connection.channel()
        self.results_channel.queue_declare(queue='{}_results'.format(self._name), durable=True)
        self.error_channel = self.connection.channel()
        self.error_channel.queue_declare(queue='{}_errors'.format(self._name), durable=True)