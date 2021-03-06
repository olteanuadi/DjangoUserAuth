from django.contrib import admin

# Register your models here.

from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_and_time')
    prepopulated_fields = {'slug':('title',)}

admin.site.register(Post, PostAdmin)