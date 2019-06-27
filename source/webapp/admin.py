from django.contrib import admin
from webapp.models import Article, Comment, UserInfo

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'author', 'created_at']

class UserInfoInline(admin.StackedInline):
    model = UserInfo



admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
