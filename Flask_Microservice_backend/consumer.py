import json
import pika
from main import Users, Posts, Comments, Tags, db

params = pika.URLParameters('')

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='django')


def callback(ch, method, properties, body):
    data = json.loads(body)
    if properties.content_type == 'tag_created':
        tag = Tags()
        db.session.add(tag)
        db.session.commit()
    elif properties.content_type == 'tag_deleted':
        db.session.query(Tags).filter(Tags.id == data).delete()
        db.session.commit()
    elif properties.content_type == 'user_created':
        user = Users()
        db.session.add(user)
        db.session.commit()
    elif properties.content_type == 'post_created':
        post = Posts(topic=data['topic'], text=data['text'],
                     likes=data['likes'], dislikes=data['dislikes'])
        db.session.add(post)
        db.session.commit()
    elif properties.content_type == 'post_updated':
        post = Posts.query.get(data['id'])
        post.topic = data['topic']
        post.text = data['text']
        post.likes = data['likes']
        post.dislikes = data['dislikes']
        post.user_id = data['user_id']
        db.session.commit()
    elif properties.content_type == 'post_deleted':
        db.session.query(Posts).filter(Posts.id == data).delete()
        db.session.commit()
    elif properties.content_type == 'comment_created':
        comment = Comments(post_id=data['post'], text=data['text'],
                           user_id=data['user_id'], likes=data['likes'],
                           dislikes=data['dislikes'])
        db.session.add(comment)
        db.session.commit()
    elif properties.content_type == 'comment_updated':
        comment = Comments.query.get(data['id'])
        comment.post_id = data['post']
        comment.text = data['text']
        comment.likes = data['likes']
        comment.dislikes = data['dislikes']
        comment.user_id = data['user_id']
        db.session.commit()
    elif properties.content_type == 'comment_deleted':
        db.session.query(Comments).filter(Comments.id == data).delete()
        db.session.commit()


channel.basic_consume(queue='django', on_message_callback=callback,
                      auto_ack=True)

channel.start_consuming()
channel.close()
