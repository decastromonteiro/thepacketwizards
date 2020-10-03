from django.db import models


class BlogCategory(models.Model):
    title = models.CharField(max_length=80)
    slug = models.SlugField(max_length=100)
    description = models.CharField(max_length=180, null=True, blank=True)

    def __str__(self):
        return self.title
