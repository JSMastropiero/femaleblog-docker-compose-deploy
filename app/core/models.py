from django.db import models
from model_utils.models import TimeStampedModel, SoftDeletableModel
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

import random
import string

from ckeditor.fields import RichTextField

# Create your models here.

class UserVerification:
    def __init__(self, email):
        self.email = email

    def create_user(self):
        user, created = User.objects.get_or_create(username=self.email, defaults={'email': self.email})
        if not created:
            token = Token.objects.get(user=user)
            return user, token
        password = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(8))
        user.set_password(password)
        user.save()
        token = Token.objects.create(user=user)
        return user, token


class Article(TimeStampedModel, SoftDeletableModel):

    title = models.CharField(
        max_length=50,
        verbose_name=('title')
    )
    description = RichTextField(
        verbose_name=('description'),
        blank=True
    )


    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=('user'),
        null=True,
        blank=True        
        
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=('is active')
    )
    tags = models.TextField(
        verbose_name=('tags'),
        blank=True
    )

    image = models.ImageField(
        verbose_name=('image'),
        blank= True
    )
    
    count = models.PositiveBigIntegerField(
        verbose_name=('count'),
        default=0

    )
    
    def num_comments(self):
        
        content_type = ContentType.objects.get_for_model(Article)
        object_id = self.pk
        return Comment.objects.filter(
            content_type=content_type, object_id=object_id).count()

    


class Comment(TimeStampedModel, SoftDeletableModel):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=('user'),
        null=True,
        blank=True 
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name=('content type'),
        null=True,
        blank=True

    ) 
    description = models.TextField(
        verbose_name=('description'),
        blank=True
    )
    object_id = models.PositiveIntegerField(
        verbose_name=('object id'),
        blank=True,
        null=True
    )
    content_object = GenericForeignKey(
        'content_type', 
        'object_id'
    )
   
    is_active = models.BooleanField(
        default=True,
        verbose_name=('is active')
    )

    class Meta():
        verbose_name = ('comment')
        verbose_name_plural = ('comments')
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
    

    def __str__(self):
        return self.description


class TypeOfFile(models.Model):

    name = models.CharField(
        max_length=50,
    )
    class Meta():
        verbose_name = ('type of file')
        verbose_name_plural = ('type of files')

    def __str__(self):
        return self.name


class File(TimeStampedModel, SoftDeletableModel):
    
    name = models.CharField(
        max_length=50,
        verbose_name=('name')
    )
    description = models.TextField(
        verbose_name=('description'),
        blank=True
    )
    size = models.IntegerField(
        verbose_name=('size'),
        null=True,
        blank=True
        
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE, 
        blank=True,
        null=True
    )
    type_of_file = models.ForeignKey(
        TypeOfFile,
        on_delete=models.CASCADE,    
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=('is active')
    )
    attachment = models.FileField(
        verbose_name=('attachment'),   
        null=True,
        blank=True  
    )

    class Meta():
        verbose_name = ('file')
        verbose_name_plural = ('files')

    def __str__(self):
        return self.name


class Profile(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=('user'),
        null=True,
        blank=True 
    )
    image = models.ImageField(
        verbose_name=('image'),
        blank= True
    )
    class Meta():
        verbose_name = ('profile')
        verbose_name_plural = ('profiles')

    def __str__(self):
        return self.user.username
    


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    AutoToken and profile default
    """
    if created:
        # create token
        Token.objects.create(user=instance)
