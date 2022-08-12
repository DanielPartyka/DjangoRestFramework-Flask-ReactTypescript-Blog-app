import pika, json

params = pika.URLParameters('')

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='django', body=json.dumps(body), properties=properties)
