__author__ = 'Alec Nunn'

import pika
import requests
from netaddr import IPNetwork
import json
from Kobold import BaseWorker


class ArinWorker(BaseWorker):

    def _arin_lookup(self, ip):
        r = requests.get('http://whois.arin.net/rest/ip/{}.json'.format(ip))
        j = json.loads(unicode(r.text))
        if 'orgRef' in r.text:
            org_name = j['net']['orgRef']['@handle']
        elif 'customerRef' in r.text:
            org_name = j['net']['customerRef']['@handle']
        else:
            return 'BROKEN:{}'.format(ip)
        return '{}:{}'.format(ip, org_name)

    def callback(self, ch, method, properties, body):
        for ip in IPNetwork(body):
            r = self._arin_lookup(ip)
            if r.split(':')[0] == 'BROKEN':
                self.error_channel.basic_publish(exchange='', routing_key='{}_errors'.format(self._name),
                                                 body=r.split(':')[1], properties=pika.BasicProperties(delivery_mode=2,))
            self.results_channel.basic_publish(exchange='', routing_key='{}_results'.format(self._name), body=r,
                                               properties=pika.BasicProperties(delivery_mode=2,))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        self.tasking_channel.basic_qos(prefetch_count=1)
        self.tasking_channel.basic_consume(self.callback, queue='{}_tasking'.format(self._name))
        self.tasking_channel.start_consuming()
