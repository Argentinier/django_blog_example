from django.contrib import admin

from .models import Post, Comment


# List of registered models


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created_at', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'compact_body', 'post', 'active', 'created_at', 'updated_at')
    list_filter = ('active', 'created_at', 'updated_at')
    raw_id_fields = ('post',)
    search_fields = ('body', 'name')
    date_hierarchy = 'created_at'
