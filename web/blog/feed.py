from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models.BlogPost import BlogPost
from django.utils import timezone


class LatestEntriesFeed(Feed):
    title = "The Packet Wizards - Seu blog de engenharia de redes e muito mais!"
    link = "/rss/"
    description = "Veja os últimos artigos públicos no The Packet Wizards Blog!"

    def items(self):
        return BlogPost.objects.order_by('-publish_date').filter(published=True, publish_date__lte=timezone.now())

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_pubdate(self, item):
        return item.publish_date

    def item_categories(self, item):
        return [item.category.title]
