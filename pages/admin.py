from django.contrib import admin
from .models import Pages

def make_published(modeladmin, request, queryset):
    queryset.update(status='p')
make_published.short_description = "Mark selected stories as published"

class PageAdmin(admin.ModelAdmin):
    save_as=True
    save_on_top=True
    view_on_site=True
    
    list_display = ['title', 'author', 'page_views', 'status', 'slug', 'order', 'created_date', 'published_date']
    ordering = ['title']
    actions = [make_published]

admin.site.register(Pages, PageAdmin)
