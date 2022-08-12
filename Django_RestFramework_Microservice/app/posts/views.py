from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Posts, Comments, Users, Tags
from .serializer import PostsSerializer, CommentsSerializer, \
    UsersSerializer, TagsSerializer
from .producer import publish
from django.contrib.auth.hashers import make_password, check_password


class TagviewSet(viewsets.ViewSet):
    # GET method (get all)
    def list(self, request):
        tags = Tags.objects.all()
        serializer = TagsSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    # POST method
    def create(self, request):
        serializer = TagsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('tag_created', serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # DELETE method
    def destroy(self, request, pk=None):
        tag = Tags.objects.get(id=pk)
        tag.delete()
        publish('tag_deleted', tag.id)
        return Response(status=status.HTTP_202_ACCEPTED)


class PostViewSet(viewsets.ViewSet):
    # GET method (get all)
    def list(self, request):
        posts = Posts.objects.all()
        serializer = PostsSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    # POST method
    def create(self, request):
        serializer = PostsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('post_created', serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # GET method
    def retrieve(self, request, pk=None):
        post = Posts.objects.all().filter(id=pk)
        serializer = PostsSerializer(post, many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    # PUT method
    def update(self, request, pk=None):
        post = Posts.objects.get(id=pk)
        serializer = PostsSerializer(instance=post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('post_updated', serializer.data)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    # DELETE method
    def destroy(self, request, pk=None):
        post = Posts.objects.get(id=pk)
        post.delete()
        publish('post_deleted', post.id)
        return Response(status=status.HTTP_202_ACCEPTED)

    # get all comments from certain post
    def get_comments(self, request, pk=None):
        post = Posts.objects.get(id=pk)
        comments = Comments.objects.filter(post=post.id)
        serializer = CommentsSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    # get a number of comments in certain post
    def get_number_of_comments(self, request, pk=None):
        post = Posts.objects.get(id=pk)
        comments = Comments.objects.filter(post=post.id)
        return Response(len(comments))

    # get a number of all posts
    def get_number_of_posts_by_tag(self, request):
        tag = request.GET['tag']
        post_by_tags = Posts.objects.filter(tags=tag)
        return Response(len(post_by_tags))

    # get a number of all post by certain tag
    def get_all_posts_number(self, request):
        tag = request.GET['tag']
        post_by_tags = Posts.objects.filter(tags=tag)
        serializer = PostsSerializer(post_by_tags, many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class CommentViewSet(viewsets.ViewSet):
    # GET method (get all)
    def list(self, request):
        comments = Comments.objects.all()
        serializer = CommentsSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    # POST method
    def create(self, request, pk=None):
        post = Posts.objects.get(id=pk)
        request.data['post'] = post.id
        serializer = CommentsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('comment_created', serializer.data)
        return Response(status=status.HTTP_201_CREATED)

    # GET method
    def retrieve(self, request, pk=None):
        comments = Comments.objects.get(id=pk)
        serializer = CommentsSerializer(comments)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    # PUT method
    def update(self, request, pk=None):
        comments = Comments.objects.get(id=pk)
        serializer = CommentsSerializer(instance=comments, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('comment_updated', serializer.data)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    # DELETE method
    def destroy(self, request, pk=None):
        comment = Comments.objects.get(id=pk)
        comment.delete()
        publish('comment_deleted', comment.id)
        return Response(status=status.HTTP_202_ACCEPTED)


class UserViewSet(viewsets.ViewSet):
    # GET method (get all)
    def list(self, request):
        user = Users.objects.all()
        serializer = UsersSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    # Get method
    def retrieve(self, request, pk=None):
        user = Users.objects.get(id=pk)
        serializer = UsersSerializer(user)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def check_credentials(self, request):
        login = request.GET['login']
        password = request.GET['password']
        try:
            user = Users.objects.get(email=login)
            if check_password(password, user.password):
                return Response('true')
            else:
                return Response('false')
        except ObjectDoesNotExist:
            return Response('false')

    # POST method
    def create(self, request):
        # in order to hash password we have to change request data to be mutable
        request.data._mutable = True
        request.data['password'] = make_password(request.data['password'])
        serializer = UsersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('user_created', serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
