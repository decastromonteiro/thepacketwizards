from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import BlogPost


class LatestEntriesFeed(Feed):
    title = "The Packet Wizards - Seu blog de engenharia de redes e muito mais!"
    link = "/rss/"
    description = "Veja os últimos artigos publicos no The Packet Wizards Blog!"

    def items(self):
        return BlogPost.objects.order_by('-publish_date')[:3]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_pubdate(self, item):
        return item.publish_date

    def item_categories(self, item):
        return [item.category.title]
