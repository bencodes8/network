from django.contrib import admin
from .models import User, Post

class UserAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("username", )}

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Post)