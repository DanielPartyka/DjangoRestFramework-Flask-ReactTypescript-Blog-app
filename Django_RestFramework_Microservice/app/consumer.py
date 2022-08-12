import pika, json, os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

from posts.models import Posts, Comments

params = pika.URLParameters('amqps://umgxzijz:IIZFy82KsbTHZDoOLeIkcLz8mVLbbggN@moose.rmq.cloudamqp.com/umgxzijz')

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='flask')


def callback(ch, method, properties, body):
    id = json.loads(body)
    if properties.content_type == 'post_liked':
        post = Posts.objects.get(id=id)
        post.likes = post.likes + 1
        post.save()
    elif properties.content_type == 'post_disliked':
        post = Posts.objects.get(id=id)
        post.dislikes = post.dislikes + 1
        post.save()
    elif properties.content_type == 'comment_liked':
        comment = Comments.objects.get(id=id)
        comment.likes = comment.likes + 1
        comment.save()
    elif properties.content_type == 'comment_disliked':
        comment = Comments.objects.get(id=id)
        comment.dislikes = comment.dislikes + 1
        comment.save()


channel.basic_consume(queue='flask', on_message_callback=callback,
                      auto_ack=True)

channel.start_consuming()
channel.close()
