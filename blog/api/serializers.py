from rest_framework import serializers
from blog.models import Post
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'title',
            'author',
            'body',
            'publish',
            'status',
        )


class PostListSerializer(serializers.ModelSerializer, TaggitSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='blog_api:detail', lookup_field='slug')
    comments = TagListSerializerField()

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'slug',
            'author',
            'body',
            'comments',
            'publish',
            'created',
            'updated',
            'url',

        )


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'slug',
            'author',
            'body',
            'publish',
            'created',
            'updated',

        )


