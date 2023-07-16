from django.contrib import admin
from . models import *


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'article_title', 'category', 'article_content', 'photo', 'pub_date', 'mod_date')
    list_display_links = ('id', 'article_title')
    search_fields = ('article_title', 'article_content')
    ordering = ['id']
    prepopulated_fields = {'slug': ('article_title',)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author_name', 'comment_text', 'added_date', 'article', 'parent_comment')
    list_display_links = ('id', 'author_name')
    search_fields = ('author_name', 'comment_text')
    ordering = ['id']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name')
    list_display_links = ('id', 'category_name')
    search_fields = ('category_name',)
    ordering = ['id']
    prepopulated_fields = {'slug': ('category_name',)}


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
