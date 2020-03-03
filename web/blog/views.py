from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.utils import timezone
from .models import BlogPost
from .forms import BlogPostForm


def home_page(request):
    title = "The Packet Wizards"
    qs = BlogPost.objects.all().order_by('-publish_date').filter(
        published=True,
        featured=True
    )[:3]
    context = {"title": title, 'blog_list': qs}
    return render(request, "index/index.html", context)


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


@login_required(login_url='/blog')
def create_blog_post(request):
    title = 'The Packet Wizards Blog'

    form = BlogPostForm()
    context = {"title": title,
               "form": form}
    return render(request, "blog/form.html", context)


def blog_post(request, slug):
    try:
        qs = BlogPost.objects.get(slug=slug)
        if qs.published and qs.publish_date < timezone.now():
            context = {"title": qs.title, 'blog_post': qs}
            return render(request, "blog/blog_post.html", context)
        return redirect('/blog')
    except Exception:
        return redirect('/blog')


def blog_category(request, category):
    now = timezone.now()
    try:
        qs = BlogPost.objects.filter(
            category__slug__exact=category
        ).order_by("-publish_date").filter(published=True,
                                           publish_date__lte=now)
        if qs:
            context = {"title": 'Category: {}'.format(category),
                       'blog_list': qs,
                       'category': qs.first().category.title,
                       'description': qs.first().category.description}
            return render(request, "blog/category.html", context)
        return redirect('/blog')
    except Exception:
        return redirect('/blog')


def blog_series(request, series):
    now = timezone.now()
    try:
        qs = BlogPost.objects.filter(
            series__slug__exact=series,
            published=True,
            publish_date__lte=now
        )
        if qs:
            context = {"title": 'Series: {}'.format(series),
                       'blog_list': qs,
                       'series': qs.first().series.title,
                       'description': qs.first().series.description}
            return render(request, "blog/series.html", context)

        return redirect('/blog')
    except Exception:
        return redirect('/blog')
