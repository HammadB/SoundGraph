import pika
import sys

def submitJob(msg):
	channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=msg,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))

channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)
message = "206905299"
submitJob(message)
print " [x] Sent %r" % (message,)
connection.close()