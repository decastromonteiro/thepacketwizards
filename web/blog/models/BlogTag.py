from django.db import models

class BlogTag(models.Model):
    tag = models.CharField(max_length=80)

    def __str__(self):
        return self.tag