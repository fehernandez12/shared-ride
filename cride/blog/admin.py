from django.contrib import admin

from cride.blog.models import Post, Status, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Post admin."""
    list_display = ('title', 'published', 'status')
    list_display_links = ('title',)
    list_editable = ('status',)
    search_fields = ('title', 'body')
    list_filter = ('status', 'created', 'modified')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Comment admin."""
    list_display = ('name', 'post', 'active')
    list_display_links = ('name', 'post')
    list_editable = ('active',)
    search_fields = ('name', 'email', 'comment')
    list_filter = ('active', 'created', 'modified')


admin.site.register(Status)
