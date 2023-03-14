from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = User
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    
    user = UserSerializer(read_only=True)
    #user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source="user")
    
    class Meta:
        model = Comment
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    num_comments = serializers.IntegerField()

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



