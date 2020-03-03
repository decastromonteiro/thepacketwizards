from django.contrib import admin
from .models import BlogPost, BlogCategory, BlogSeries, Author
from markdownx.admin import MarkdownxModelAdmin

# Register your models here.


admin.site.register(BlogPost, MarkdownxModelAdmin)
admin.site.register(BlogSeries)
admin.site.register(BlogCategory)
admin.site.register(Author)
