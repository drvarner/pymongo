from flask import Flask, jsonify
from flask.views import MethodView
from mongoengine import connect

from mongo import Post, PostSchema

connect('tumblelog')

app = Flask(__name__)


class PostView(MethodView):

    def get(self):
        post_schema = PostSchema(many=True)
        posts = Post.objects
        dump_data = post_schema.dump(posts)

        return jsonify(dump_data)

    def post(self):
        pass


post_view = PostView.as_view('post_view')
app.add_url_rule('/posts', view_func=post_view, methods=['GET', 'POST'])


if __name__ == '__main__':
    app.run(debug=True)
