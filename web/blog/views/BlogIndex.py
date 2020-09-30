from django.utils import timezone
from ..schemas.BlogPost import BlogPost
from django.core.paginator import Paginator
from django.shortcuts import render


def blog_index(request):
    title = "Blog - The Packet Wizards"
    now = timezone.now()
    qs = BlogPost.objects.all().order_by('-publish_date').filter(published=True,
                                                                 publish_date__lte=now)
    paginator = Paginator(qs, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    context = {"title": title, 'blog_list': posts}
    
    
    
    return render(request, "blog/index.html", context)
