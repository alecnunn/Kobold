# -*- coding: utf-8 -*-
import pika

class BaseWorker(object):
    def __init__(self, hostname, *args, **kwargs):
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host=hostname))
        self.channel = self.conn.channel()
        self.channel.exchange_declare(exchange='kobold', type='topic')
        self.result = self.channel.queue_declare(exclusive=True)
        self.queue_name = self.result.method.queue
        self.task_type = kwargs['type']
        self.task_name = kwargs['name']
        self.priority = kwargs['priority']
        self.work_body = kwargs['body']
        self.keys = {'tasks': '', 'results': '', 'errors': ''}

    def SetPriority(self, priority):
        self.priority = priority.lower()

    def Initialize(self):
        binding_keys = ['tasks', 'results', 'errors']
        for binding_key in binding_keys:
            self.channel.queue_bind(exchange='kobold', queue=self.queue_name, routing_key="{}.{}.{}.{}".format(self.priority, self.task_type, self.task_name, binding_key))
            self.keys[binding_key] = "{}.{}.{}.{}".format(self.priority, self.task_type, self.task_name, binding_key)

    def DoWork(self, ch, method, properties, body):
        results = {}
        self.PushResults(results)

    def PushResults(self, msg, success=True):
        rKey = self.keys['results'] if success else self.keys['errors']
        self.channel.basic_publish(exchange='kobold', routing_key=rKey, body=msg)



"""
sample message structure

{
    "job": "arin",              // the task type that will be used
    "version": "1.0.0",         // the version of the task that will be used
    "job-name": "test",         // the user defined name for this instance
    "body": {                   // the body that will be parsed by the workers
        "params": "1.2.3.4/24"  // the workers will be responsible for parsing and using this info
    }
}
"""