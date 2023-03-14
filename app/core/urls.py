from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('api/user', UserViewset)
router.register('api/article', ArticleViewset)
router.register('api/comment', CommentViewset)
router.register('api/file', FileViewset)
router.register('api/type_of_file', TypeOfFileViewset)
router.register('api/profile', Profile)



urlpatterns = router.urls