from django.db import models
from django.urls import reverse
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from django.utils.text import slugify
from .Author import Author
from .BlogSeries import BlogSeries
from .BlogCategory import BlogCategory
from .BlogTag import BlogTag
from .TwitterPost import TwitterPost

import re
import math
from django.utils.html import strip_tags
from uuid import uuid4


class BlogPost(models.Model):
    title = models.CharField(max_length=80)
    slug = models.SlugField(unique=True, editable=True, max_length=100, blank=True, null=True)
    description = models.CharField(max_length=180)
    thumbnail = models.ImageField(blank=True, null=True)
    thumbnail_alt_text = models.CharField(max_length=80, null=True, blank=True)
    content = MarkdownxField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    publish_date = models.DateTimeField(null=True, blank=True)
    series_index = models.IntegerField(null=True, blank=True)
    read_time = models.IntegerField(null=True, blank=True)
    twitter_uuid = models.UUIDField(null=True, blank=True)
    twitter_content = models.TextField(max_length=257, null=True, blank=True)

    # Relations
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, default=1)
    series = models.ForeignKey(BlogSeries, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(BlogTag, blank=True)

    def formatted_markdown(self):
        """
        Transform content into HTML code
        """
        return markdownify(self.get_clean_content())

    def get_truncated_content(self):
        """
        Get content between ::begin:: and ::more:: Tags and return it.
        """
        pattern = re.compile(r"(?<=::begin::)(.*)(?=::more::)", re.DOTALL)
        truncated = self.content[:300]
        if "::more::" in self.content:
            truncated = re.search(pattern, self.content)
            if truncated:
                return markdownify(truncated.group())
        return markdownify(truncated)

    def get_clean_content(self):
        """
        Get content field and rip it off from ::more:: and ::begin:: Tags
        Return Content without those tags.
        """
        return self.content.replace("::more::", "").replace("::begin::", "")

    def get_read_time(self):
        word_count = len(re.findall(r"\w+", strip_tags(self.formatted_markdown())))
        read_time_min = math.ceil(word_count / 200)  # 200 Words Per Minute
        return read_time_min

    def get_absolute_url(self):
        return reverse("blogpost", args=[self.slug])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)

        if not self.twitter_uuid:
            self.twitter_uuid = uuid4()

        if self.twitter_content:
            if self.published:
                try:
                    twitter_update = TwitterPost.objects.get(uuid=self.twitter_uuid)
                    twitter_update.content = self.twitter_content
                    twitter_update.publish_date = self.publish_date
                    twitter_update.post_url = self.get_absolute_url()
                    twitter_update.save()
                except TwitterPost.DoesNotExist:
                    twitter_update = TwitterPost(
                        uuid=self.twitter_uuid,
                        content=self.twitter_content,
                        publish_date=self.publish_date,
                        post_url=self.get_absolute_url(),
                    )
                    twitter_update.save()

        self.read_time = self.get_read_time()

        super().save(*args, **kwargs)
