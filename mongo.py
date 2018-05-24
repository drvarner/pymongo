from mongoengine import connect, \
    Document, EmbeddedDocument, \
    StringField, ReferenceField, ListField, EmbeddedDocumentField, \
    CASCADE
from marshmallow_mongoengine import ModelSchema

connect('tumblelog')


class User(Document):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)


class Comment(EmbeddedDocument):
    content = StringField()
    name = StringField(max_length=120)


class Post(Document):
    title = StringField(max_length=120, required=True)
    author = ReferenceField(User, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=30))
    comments = ListField(EmbeddedDocumentField(Comment))

    meta = {'allow_inheritance': True}


class PostSchema(ModelSchema):
    class Meta:
        model = Post


class TextPost(Post):
    content = StringField()


class ImagePost(Post):
    image_path = StringField()


class LinkPost(Post):
    link_url = StringField()


if not User.objects:
    ross = User(
        email='ross@example.com',
        first_name='Ross',
        last_name='Lawley'
    )

    dave = User(
        email='david.r.varner@gmail.com',
        first_name='David',
        last_name='Varner'
    )

    ross.save()
    dave.save()

if not Post.objects:
    post1 = TextPost(title='Fun with MonoEngine', author=dave)
    post1.content = 'Took a look at MonoEngine today, looks pretty cool.'
    post1.tags = ['mongodb', 'mongoengine']
    post1.comments.append(Comment(name='Admin', content="This post is great!"))
    post1.save()

    post2 = LinkPost(title='MonoEngine Documentation', author=ross)
    post2.link_url = 'https://docs.mongoengine.com/'
    post2.tags = ['mongoengine']
    post2.save()

for post in Post.objects:
    print(post.title)
    print('=' * len(post.title))

    if isinstance(post, TextPost):
        print("id: {}".format(post.id))
        print("{} - {}".format(post.content, post.author.first_name))
        print('-- Comments --')
        print('{} - {}'.format(
            post.comments[0].content, post.comments[0].name))

    if isinstance(post, LinkPost):
        print("id: {}".format(post.id))
        print('Link: {}'.format(post.link_url))
