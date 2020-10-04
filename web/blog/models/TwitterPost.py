from django.db import models
from ..tasks import twitter_post
from django.utils import timezone
from thepacketwizards.celery import app


class TwitterPost(models.Model):
    uuid = models.UUIDField(unique=True, null=False)
    content = models.TextField(max_length=257, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(null=True, blank=True)
    post_url = models.CharField(max_length=100, blank=True, null=True)
    task_id = models.UUIDField(blank=True, null=True)

    __original_content = None
    __original_publish_date = None
    __original_post_url = None

    def include_blog_url(self):
        return self.content.replace("{{post}}", f"https://thepacketwizards.com{self.post_url}")

    def __init__(self, *args, **kwargs):
        super(TwitterPost, self).__init__(*args, **kwargs)
        self.__original_content = self.content
        self.__original_publish_date = self.publish_date
        self.__original_post_url = self.post_url

    def save(self, *args, **kwargs):
        content = self.include_blog_url()
        if not self.id:
            if timezone.now() <= self.publish_date:
                task = twitter_post.apply_async(kwargs={"status": content}, eta=self.publish_date)
                self.task_id = task.id
            else:
                task = twitter_post.delay(content)
                self.task_id = task.id
        elif (
            (self.content != self.__original_content)
            or (self.publish_date != self.__original_publish_date)
            or (self.post_url != self.__original_post_url)
        ):
            if timezone.now() <= self.publish_date:
                if not self.task_id:
                    task = twitter_post.apply_async(kwargs={"status": content}, eta=self.publish_date)
                    self.task_id = task.id
                else:
                    app.control.revoke(str(self.task_id))
                    task = twitter_post.apply_async(kwargs={"status": content}, eta=self.publish_date)
                    self.task_id = task.id
            else:
                if not self.task_id:
                    task = twitter_post.delay(content)
                    self.task_id = task.id
                else:
                    app.control.revoke(str(self.task_id))
                    task = twitter_post.delay(content)
                    self.task_id = task.id

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):

        app.control.revoke(str(self.task_id))

        super().delete(*args, **kwargs)
