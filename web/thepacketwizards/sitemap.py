from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import BlogPost


class BlogSiteMap(Sitemap):
    changefreq = 'never'

    def items(self):
        return BlogPost.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.publish_date


class StaticSiteMap(Sitemap):
    changefreq = 'yearly'

    def items(self):
        return ['home']

    def location(self, item):
        return reverse(item)
