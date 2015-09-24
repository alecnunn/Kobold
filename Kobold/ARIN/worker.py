__author__ = 'Alec Nunn'

import requests
from netaddr import IPNetwork
import json
from Kobold.Base import BaseWorker


class ArinWorker(BaseWorker):
    """ArinWorker is a fairly simple example worker to scrape ARIN's REST interface for ownership information of IPs"""
    def arin_lookup(self, ip):
        r = requests.get('http://whois.arin.net/rest/ip/{}.json'.format(ip))
        j = json.loads(unicode(r.text))
        if 'orgRef' in r.text:
            org_name = j['net']['orgRef']['@handle']
        elif 'customerRef' in r.text:
            org_name = j['net']['customerRef']['@handle']
        else:
            return 'BROKEN:{}'.format(ip)
        return '{}:{}'.format(ip, org_name)

    def DoWork(self, ch, method, properties, body):
        for ip in IPNetwork(body):
            r = self.arin_lookup(ip)
            if r.split(':')[0] == 'BROKEN':
                self.PushResults(r, False)
            self.PushResults(r, True)
        ch.basic_ack(delivery_tag=method.delivery_tag)

if __name__ == '__main__':
    worker = ArinWorker('localhost', 'test')
    worker.run()
