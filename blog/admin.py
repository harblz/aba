from django.contrib import admin
from .models import Post, Category

def make_published(modeladmin, request, queryset):
    queryset.update(status='p')
make_published.short_description = "Mark selected stories as published"

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'page_views', 'status', 'slug', 'snippet_size', 'created_date', 'published_date']
    ordering = ['title']
    actions = [make_published]



class CategoryInline(admin.TabularInline):
    model = Category
admin.site.register(Category)

admin.site.register(Post, PostAdmin)
