"""thepacketwizards URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from blog.feed import LatestEntriesFeed
from blog.views import (blog_index,
                        blog_post,
                        blog_category,
                        blog_series, create_blog_post)

urlpatterns = [
    path("", blog_index),
    path('create/', create_blog_post),
    path("<slug:slug>/", blog_post, name='blogpost'),
    path("category/<slug:category>", blog_category),
    path("series/<slug:series>", blog_series),
    path('rss', LatestEntriesFeed())
]
