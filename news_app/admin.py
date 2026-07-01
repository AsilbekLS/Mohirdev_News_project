from django.contrib import admin

from news_app.models import News, Category, Contacts


# Register your media here.

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title','slug','published_time','status']
    list_filter = ['status','created_time','published_time']
    prepopulated_fields = {'slug':('title',)}
    date_hierarchy = 'published_time'
    search_fields = ['title','body']
    ordering = ['status', 'published_time']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name']

admin.site.register(Contacts)