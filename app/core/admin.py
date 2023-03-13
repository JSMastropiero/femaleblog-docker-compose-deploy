from django.contrib import admin
from .models import Article, Comment, File, TypeOfFile, Profile

admin.site.site_header = "Administrador Female Christi"
admin.site.site_title = " Female Christi"
admin.site.index_title = "Bienvenida"

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    search_fields = [
        'title',
        'tags',
    ]
    list_display = ['title','id', 'created', 'modified', 'is_active', 'user', 'count' ]
    #autocomplete_fields = ['charger']


class CommentAdmin(admin.ModelAdmin):
    search_fields = [
        'user',
        
    ]
    list_display = ['id', 'user', 'created', 'modified']
    #autocomplete_fields = ['charger']


class FileAdmin(admin.ModelAdmin):
    search_fields = [
        'name',
        'user',
        'type_of_file'

        
    ]
    list_display = ['id', 'user', 'type_of_file','is_active', 'created', 'modified']
    #autocomplete_fields = ['charger']


class ProfileAdmin(admin.ModelAdmin):
    search_fields = [
        'user',
        
    ]
    list_display = ['id', 'user', 'created', 'modified']
    #autocomplete_fields = ['charger']


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
admin.site.register(File)
admin.site.register(TypeOfFile)
admin.site.register(Profile)

