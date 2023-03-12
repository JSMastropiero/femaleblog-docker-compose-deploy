from django.contrib import admin
from .models import Article, Comment, File, TypeOfFile, Profile

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    search_fields = [
        'title',
        'tags',
    ]
    list_display = ['title','id', 'created', 'modified', 'is_active', 'user', 'count' ]
    #autocomplete_fields = ['charger']


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
admin.site.register(File)
admin.site.register(TypeOfFile)
admin.site.register(Profile)

