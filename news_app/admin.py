from django.contrib import admin

from news_app.models import News, Category, Contacts, Comment


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

class CommentAdmin(admin.ModelAdmin):
    list_display = ['user','body','created_time','active']
    list_filter = ['active','created_time']
    search_fields = ['user','body']
    actions = ['disable_comment','activate_comment']

    def disable_comment(self,request,queryset):
        queryset.update(active=False)

    def activate_comment(self,request,queryset):
        queryset.update(active=True)

admin.site.register(Comment,CommentAdmin)