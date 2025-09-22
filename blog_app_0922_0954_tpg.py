# 代码生成时间: 2025-09-22 09:54:51
from django.db import models
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.urls import path

"""
A Django application component for a simple blog with models, views, and URLs.
"""

class Post(models.Model):
    """
    A blog post model.
    """
    title = models.CharField(max_length=200, help_text="Enter a title for your blog post.")
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['published_date']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


def post_list(request):
    """
    View function to display a list of all blog posts.
    """
    posts = Post.objects.all().order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    """
    View function to display detail of a single blog post.
    """
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        raise Http404("Post does not exist")
    return render(request, 'blog/post_detail.html', {'post': post})

# Define the URL patterns
urlpatterns = [
    path('blog/', post_list, name='post_list'),
    path('blog/<int:pk>/', post_detail, name='post_detail'),
]
