from django.contrib import admin
from .models import Post

class PostModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'timestamp', 'updates', ]
    list_display_links = ['updates',]
    list_editable = ['title']
    list_filter = ['timestamp', 'updates']
    search_fields = ['title','content']
    class Meta:
        model = Post

admin.site.register(Post, PostModelAdmin)
