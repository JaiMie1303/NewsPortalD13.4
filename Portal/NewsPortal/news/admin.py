from django.contrib import admin
from .models import Category, Post, Author, PostCategory, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_published', 'category')
    list_filter = ('author', 'date_published', 'category')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-date_published',)
    actions = ['make_published', 'make_draft']

    def make_published(self, request, queryset):
        queryset.update(status='published')
        self.message_user(request, 'Выбранные записи были успешно опубликованы.')

    make_published.short_description = 'Сделать выбранные записи опубликованными.'


admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Author)
admin.site.register(PostCategory)
admin.site.register(Comment)
