from django.contrib import admin
from home.models import Event, GoodSite, Category, HomeInfo
from article.admin import ArticleInline

class CategoryAdmin(admin.ModelAdmin):
    fields=['name', 'displayed_name', 'comment']

class GoodSiteAdmin(admin.ModelAdmin):
    fields=['name', 'comment', 'link']

class EventAdmin(admin.ModelAdmin):
    fields=['name', 'pub_date', 'category', 'image', 'is_pinned']
    inlines = [ArticleInline]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(GoodSite, GoodSiteAdmin)
admin.site.register(HomeInfo)
