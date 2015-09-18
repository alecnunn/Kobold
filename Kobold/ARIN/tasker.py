__author__ = 'Alec Nunn'

import pika

class ArinTasker(object):
    def __init__(self, hostname, name=''):
        self._name = name if name != '' else self.__class__.__name__
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host=hostname))
        self.channel = self.conn.channel()
        self.channel.queue_declare(queue='{}_tasking'.format(self._name))

    def send_task(self, task):
        self.channel.basic_publish(exchange='', routing_key='{}_tasking'.format(self._name), body=task,
                                   properties=pika.BasicProperties(delivery_mode=2,))

if __name__ == '__main__':
    import sys

    tasker = ArinTasker('localhost')

    with open(sys.argv[0], 'r') as f:
        for line in f:
            tasker.send_task(line.rstrip('\r\n'))
            print " [x] Sent {}".format(line.rstrip('\r\n'))
    tasker.conn.close()
