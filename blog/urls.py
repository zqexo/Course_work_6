from django.urls import path

from blog.apps import BlogConfig
from blog.views import (
    BlogListView,
    BlogCreateView,
    BlogUpdateView,
    BlogDeleteView,
    BlogDetailView,
)

app_name = BlogConfig.name

urlpatterns = [
    path("", BlogListView.as_view(), name="blog_list"),
    path("blog/new", BlogCreateView.as_view(), name="blog_create"),
    path("blog/edit/<int:pk>", BlogUpdateView.as_view(), name="blog_update"),
    path("blog/detail/<int:pk>", BlogDetailView.as_view(), name="blog_detail"),
    path("blog/delete/<int:pk>", BlogDeleteView.as_view(), name="blog_delete"),
]
