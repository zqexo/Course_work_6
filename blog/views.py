from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DeleteView,
    UpdateView,
    CreateView,
    DetailView,
)
from django.core.cache import cache

from blog.forms import BlogForm
from blog.models import Blog
from blog.services import get_blogs_from_cache


class BlogListView(LoginRequiredMixin, ListView):
    model = Blog
    extra_context = {"title": "Сообщения"}

    def get_queryset(self):
        """Получаем блоги из кэша, если кэш пуст, получаем данные из БД."""
        return get_blogs_from_cache()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_create_blogpost"] = self.request.user.has_perm(
            "blog.can_create_blogpost"
        )
        context["can_update_blogpost"] = self.request.user.has_perm(
            "blog.can_update_blogpost"
        )
        context["can_delete_blogpost"] = self.request.user.has_perm(
            "blog.can_delete_blogpost"
        )
        return context


class BlogCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    permission_required = "blog.can_create_blogpost"
    success_url = reverse_lazy("blog:blog_list")

    def form_valid(self, form):
        cache.clear()
        form.instance.user = self.request.user
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    permission_required = "blog.can_update_blogpost"
    success_url = reverse_lazy("blog:blog_list")

    def form_valid(self, form):
        cache.clear()
        return super().form_valid(form)


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy("blog:blog_list")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()
        return self.object


class BlogDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Blog
    permission_required = "blog.can_delete_blogpost"
    success_url = reverse_lazy("blog:blog_list")

    def form_valid(self, form):
        cache.clear()
        return super().form_valid(form)
