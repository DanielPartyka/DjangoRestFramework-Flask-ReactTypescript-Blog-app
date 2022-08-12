import requests
from flask import Flask, jsonify, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from producer import publish

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@db/main'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Tags(db.Model):
    __tablename__ = 'Tags'
    id = id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = text = db.Column(db.String(40))
    posts = db.relationship('Posts', backref='Tags')


class Posts(db.Model):
    __tablename__ = 'Posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(250))
    text = db.Column(db.String(1000))
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)
    comments = db.relationship('Comments', backref='Posts')
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('Tags.id'))


class Users(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(300))
    nickname = db.Column(db.String(100))
    comments = db.relationship('Comments', backref='Users')
    posts = db.relationship('Posts', backref='Users')


class Comments(db.Model):
    __tablename__ = 'Comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(1000))
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)
    post_id = db.Column(db.Integer, db.ForeignKey('Posts.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))


def get_posts_request(id):
    request = requests.get(f'http://host.docker.internal:8000/api/posts/{id}')
    data_as_json = request.json()
    return data_as_json


def get_comments_request(id):
    request = requests.get(f'http://host.docker.internal:8000/api/comments/{id}')
    data_as_json = request.json()
    return data_as_json


# like post
@app.route('/api/posts/<int:id>/like', methods=['POST'])
def like_post(id):
    data_as_json = get_posts_request(id)
    try:
        post = Posts.query.get(int(data_as_json[0]['id']))
        value = int(post.likes)
        post.likes = value + 1
        db.session.commit()
        publish('post_liked', id)
    except:
        abort(400, 'Something went wrong')
    return jsonify({
        'message': 'success'
    })


# dislike post
@app.route('/api/posts/<int:id>/dislike', methods=['POST'])
def dislike_post(id):
    data_as_json = get_posts_request(id)
    try:
        post = Posts.query.get(data_as_json[0]['id'])
        value = int(post.dislikes)
        post.dislikes = value + 1
        db.session.commit()
        publish('post_disliked', id)
    except:
        abort(400, 'Something went wrong')
    return jsonify({
        'message': 'success'
    })


# like comment
@app.route('/api/comments/<int:id>/like', methods=['POST'])
def like_comment(id):
    data_as_json = get_comments_request(id)
    try:
        comment = Comments.query.get(data_as_json['id'])
        value = int(comment.likes)
        comment.likes = value + 1
        publish('comment_liked', id)
        db.session.commit()
    except:
        abort(400, 'Something went wrong')
    return jsonify({
        'message': 'success'
    })


# dislike comment
@app.route('/api/comments/<int:id>/dislike', methods=['POST'])
def dislike_comment(id):
    data_as_json = get_comments_request(id)
    try:
        comment = Comments.query.get(data_as_json['id'])
        value = int(comment.dislikes)
        comment.dislikes = value + 1
        db.session.commit()
        publish('comment_disliked', id)
    except:
        abort(400, 'Something went wrong')
    return jsonify({
        'message': 'success'
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
