from flask import Flask
from flask import make_response
from flask.views import MethodView
from mongoengine import connect

from mongo import Post

connect('tumblelog')

app = Flask(__name__)


class PostView(MethodView):

    def get(self):
        response = make_response(Post.objects.to_json())
        response.headers['Content-Type'] = 'application/json'
        return response


post_view = PostView.as_view('post_view')
app.add_url_rule('/posts', view_func=post_view, methods=['GET'])


if __name__ == '__main__':
    app.run(debug=True)
