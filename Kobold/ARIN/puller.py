__author__ = 'Alec Nunn'

import socket
import sqlite3
import struct
from Kobold.Kobold import BaseWorker


class ArinPuller(BaseWorker):
    """ArinPuller is a basic worker that pulls the results from ArinWorker and stores the results in a database"""
    def ip_to_dec(self, ip):
        return struct.unpack('!I', socket.inet_aton(str(ip)))[0]

    def get_db(self):
        return sqlite3.connect('arin.db', isolation_level=None)

    def init_db(self):
        db = self.get_db()
        db.executescript("create table 'arin' ('ip' integer', 'org' text);")
        db.close()

    def query(self, q, args=(), one=False):
        cur = self.get_db().execute(q, args)
        r = cur.fetchall()
        return (r[0] if r else None) if one else r

    def insert(self, ip, org):
        return self.query('insert into arin values (?, ?)', [self.ip_to_dec(ip), org])

    def callback(self, ch, method, properties, body):
        v = body.split(':')
        self.insert(v[0], v[1])
        ch.basic_ack(delivery_tag=method.deliver_tag)

    def run(self):
        self.results_channel.basic_qos(prefetch_count=1)
        self.results_channel.basic_consume(self.callback, queue='{}_results'.format(self._name))
        self.results_channel.start_consuming()