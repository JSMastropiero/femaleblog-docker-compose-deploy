from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = User
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Comment
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    comments = CommentSerializer(many=True, read_only=True)
    num_comments = serializers.IntegerField(source='num_comments', read_only=True)
    
    
    class Meta:
        model = Article
        fields = '__all__'
        





class TypeOfFileSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = TypeOfFile
        fields = '__all__'


class FileSerializer(serializers.ModelSerializer):
    type_of_file = TypeOfFileSerializer(read_only=True)
    type_of_file_id = serializers.PrimaryKeyRelatedField(queryset=TypeOfFile.objects.all(), source="type_of_file")

    class Meta:
        model = File
        fields = '__all__'