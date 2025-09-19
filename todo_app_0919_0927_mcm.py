# 代码生成时间: 2025-09-19 09:27:08
from django.db import models
from django.shortcuts import render, redirect
from django.urls import path
from django.views import View
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods

# 数据模型
class Todo(models.Model):
    """
    Todo model to store information about tasks.
    """
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
# NOTE: 重要实现细节
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String representation of the Todo instance."""
        return self.title

# 视图
class TodoListView(View):
    """
# 扩展功能模块
    View to display a list of all todos.
    """
    def get(self, request, *args, **kwargs):
        todos = Todo.objects.all().order_by('-created_at')
        return render(request, 'todos/todo_list.html', {'todos': todos})
# 改进用户体验

class TodoDetailView(View):
    """
    View to display details of a specific todo.
    """
    @require_http_methods(['GET'])  # 限制HTTP方法
    def get(self, request, pk, *args, **kwargs):
        try:
            todo = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            raise Http404('Todo not found')
        return render(request, 'todos/todo_detail.html', {'todo': todo})

class TodoCreateView(View):
    """
    View to create a new todo.
    """
    @require_http_methods(['POST'])  # 限制HTTP方法
# 优化算法效率
    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        todo = Todo(title=title)
        todo.save()
        return redirect('todo_list')
# 改进用户体验

# URL配置
urlpatterns = [
    path('todos/', TodoListView.as_view(), name='todo_list'),
    path('todos/<int:pk>/', TodoDetailView.as_view(), name='todo_detail'),
    path('todos/new/', TodoCreateView.as_view(), name='todo_create'),
]
# FIXME: 处理边界情况
