from flask import Flask, jsonify, request
from flask.views import MethodView
from mongoengine import connect

from mongo import Post, PostSchema

connect('tumblelog')

app = Flask(__name__)


class PostView(MethodView):

    def get(self, post_id):
        if post_id is None:
            post_schema = PostSchema(many=True)
            posts = Post.objects
            dump_data = post_schema.dump(posts)

            return jsonify(dump_data)

        else:
            post_schema = PostSchema()
            post = Post.objects.get(id=post_id)
            dump_data = post_schema.dump(post)

            return jsonify(dump_data)

    def post(self):
        post_schema = PostSchema()
        posted_post = post_schema.load(request.get_json()).data

        posted_post.save()
        dump_data = post_schema.dump(posted_post)

        return jsonify(dump_data)

    def delete(self, post_id):
        post = Post.objects.get(id=post_id)
        post.delete()

        return jsonify('{"message": "Post deleted"}')

    def put(self, post_id):
        pass


def register_api(view, endpoint, url, pk='id'):
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None}, view_func=view_func,
                     methods=['GET'])
    app.add_url_rule(url, view_func=view_func, methods=['POST'])
    app.add_url_rule(f'{url}<{pk}>', view_func=view_func,
                     methods=['GET', 'PUT', 'DELETE'])


register_api(PostView, 'post_view', '/posts/', pk='post_id')

# post_view = PostView.as_view('post_view')
# app.add_url_rule('/posts/', defaults={'post_id': None},
#                  view_func=post_view, methods=['GET'])
# app.add_url_rule('/posts/', view_func=post_view, methods=['POST'])
# app.add_url_rule('/posts/<post_id>', view_func=post_view,
#                  methods=['GET', 'PUT', 'DELETE'])


if __name__ == '__main__':
    app.run(debug=True)
