from django.db import models


class BlogSeries(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField(max_length=180, null=True, blank=True)
    slug = models.SlugField(unique=True, max_length=100)

    def __str__(self):
        return self.title
