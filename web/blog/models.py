from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from django.utils.text import slugify

import re
import math
from django.utils.html import strip_tags


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def get_name(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)

    def __str__(self):
        return self.get_name()


# Create your models here.
class BlogSeries(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField(max_length=180, null=True, blank=True)
    slug = models.SlugField(unique=True, max_length=100)

    def __str__(self):
        return self.title


class BlogCategory(models.Model):
    title = models.CharField(max_length=80)
    slug = models.SlugField(max_length=100)
    description = models.CharField(max_length=180, null=True, blank=True)

    def __str__(self):
        return self.title


class BlogPost(models.Model):
    title = models.CharField(max_length=80)
    slug = models.SlugField(unique=True, editable=True, max_length=100, blank=True, null=True)
    description = models.CharField(max_length=180)
    thumbnail = models.ImageField(blank=True, null=True)
    content = MarkdownxField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    publish_date = models.DateTimeField(null=True, blank=True)
    series_index = models.IntegerField(null=True, blank=True)
    read_time = models.IntegerField(null=True, blank=True)

    # Relations
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, default=1)
    series = models.ForeignKey(BlogSeries, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True)

    def formatted_markdown(self):
        """
        Transform content into HTML code
        """
        return markdownify(self.get_clean_content())

    def get_truncated_content(self):
        """
        Get content between ::begin:: and ::more:: Tags and return it.
        """
        pattern = re.compile(r'(?<=::begin::)(.*)(?=::more::)', re.DOTALL)
        truncated = self.content[:300]
        if '::more::' in self.content:
            truncated = re.search(pattern, self.content)
            if truncated:
                return markdownify(truncated.group())
        return markdownify(truncated)

    def get_clean_content(self):
        """
        Get content field and rip it off from ::more:: and ::begin:: Tags
        Return Content without those tags.
        """
        return self.content.replace('::more::', '').replace('::begin::', '')

    def get_read_time(self):
        word_count = len(re.findall(r'\w+', strip_tags(self.formatted_markdown())))
        read_time_min = math.ceil(word_count / 200)  # 200 Words Per Minute
        return read_time_min

    def get_absolute_url(self):
        return reverse('blogpost', args=[self.slug])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        self.read_time = self.get_read_time()

        super().save(*args, **kwargs)
