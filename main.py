import pymysql
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from google.cloud import pubsub_v1


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://cloudsql:app1123@127.0.0.1:3308/app_users'
db = SQLAlchemy(app)

project = 'sacred-highway-197822'
topic_name = 'new_user'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

# db.create_all()


def serialize(user):
    return {
        'username':user.username,
        'email':user.email
    }

def publish_messages():
    """Publishes multiple messages to a Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project, topic_name)

    for n in range(1, 10):
        data = u'Message number {}'.format(n)
        # Data must be a bytestring
        data = data.encode('utf-8')
        publisher.publish(topic_path, data=data)

    print('Published messages.')

@app.route("/users")
def hello():
    users = User.query.all()
    data = []
    for item in users:
        data.append(serialize(item))
    publish_messages()
    return jsonify(json_list = data)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8081, debug=True)