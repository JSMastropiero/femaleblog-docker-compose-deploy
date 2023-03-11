from itertools import count
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework import viewsets
from .serializers import *
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from .pagination import *
from .models import UserVerification
from rest_framework.views import APIView




# Create your views here.

class CustomAuthToken(ObtainAuthToken):
    """
    Custom export user token
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        # create token
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key
        })


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('username', 'first_name', 'last_name')

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        user_verification = UserVerification(email)
        user, token = user_verification.create_user()
        serializer = self.get_serializer(user)
        return Response({'user': serializer.data, 'token': token.key})



class ArticleViewset(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title','description', 'tags', 'user__username', 'user__first_name', 'user__last_name')
    pagination_class = ArticlePagination

    def retrieve(self, request, pk):
         obj = self.get_object()
         obj.count = obj.count+1
         obj.save()
         serializer = self.get_serializer(obj)
         return Response(serializer.data)

    def get_queryset(self):
        queryset = Article.objects.all().annotate(num_comments=count('comments'))
        return queryset
    

    
    
   


class CommentViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['id', 'content_type', 'object_id']
    pagination_class = CommentPagination


class TypeOfFileViewset(viewsets.ModelViewSet):
    queryset = TypeOfFile.objects.all()
    serializer_class = TypeOfFileSerializer
    

class FileViewset(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name', 'description', 'user__username', 'user__first_name','user__last_name', 'type_of_file__name')
    pagination_class = FilePagination

class ProfileViewset(viewsets.ModelViewSet):
    queryset = Profile.objects.all()


class ArticleCommentCount(APIView):
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
