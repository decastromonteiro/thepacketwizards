from django.shortcuts import render
from blog.models import BlogPost
from django.utils import timezone

def home_page(request):
    title = "The Packet Wizards"
    now = timezone.now()
    qs = BlogPost.objects.all().order_by('-publish_date').filter(
        published=True,
        featured=True,
        publish_date__lte=now
    )[:3]
    context = {"title": title, 'blog_list': qs}
    return render(request, "index/index.html", context)