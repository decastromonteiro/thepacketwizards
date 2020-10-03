from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models.BlogPost import BlogPost
from .models.BlogCategory import BlogCategory
from .models.BlogSeries import BlogSeries
from .models.Author import Author
from .models.BlogTag import BlogTag
from .models.TwitterPost import TwitterPost


# Register your models here.
admin.site.register(BlogPost, MarkdownxModelAdmin)
admin.site.register(BlogSeries)
admin.site.register(BlogCategory)
admin.site.register(Author)
admin.site.register(BlogTag)
admin.site.register(TwitterPost)
