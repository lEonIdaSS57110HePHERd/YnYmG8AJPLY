# 代码生成时间: 2025-09-21 05:20:29
{
    "models.py": """
    # models.py
    from django.db import models
    
    class SecureModel(models.Model):
        # Example model with fields
        name = models.CharField(max_length=100)
        value = models.IntegerField()
        
        class Meta:
            verbose_name = "Secure Model"
            verbose_name_plural = "Secure Models"
        
        def __str__(self):
            return self.name
    """,
    "views.py": """
    # views.py
    from django.shortcuts import render, get_object_or_404
    from django.http import HttpResponse, Http404
    from .models import SecureModel
    from django.db.models import Q
    
    # Create your views here.
    def secure_list(request):
        """
        View to list all SecureModel instances.
        
        Uses Django ORM to prevent SQL injection.
        """
        objects = SecureModel.objects.all()
        return render(request, 'secure_app/secure_list.html', {'objects': objects})
    
    def secure_detail(request, pk):
        """
        View to retrieve a SecureModel instance by its primary key.
        
        Uses Django ORM to prevent SQL injection.
        """
        try:
            obj = SecureModel.objects.get(pk=pk)
        except SecureModel.DoesNotExist:
            raise Http404("SecureModel does not exist")
        
        return render(request, 'secure_app/secure_detail.html', {'obj': obj})
    
    def secure_search(request):
        """
        View to search SecureModel instances by name.
        
        Uses Django ORM Q objects to prevent SQL injection.
        """
        query = request.GET.get('q')
        if query:
            objects = SecureModel.objects.filter(
                Q(name__icontains=query) | Q(value=query)
            )
        else:
            objects = SecureModel.objects.none()
        return render(request, 'secure_app/secure_search.html', {'objects': objects})
    """,
    "urls.py": """
    # urls.py
    from django.urls import path
    from . import views
    
    urlpatterns = [
        path('', views.secure_list, name='secure_list'),
        path('<int:pk>/', views.secure_detail, name='secure_detail'),
        path('search/', views.secure_search, name='secure_search'),
    ]
    """
}