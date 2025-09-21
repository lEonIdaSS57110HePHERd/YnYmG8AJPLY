# 代码生成时间: 2025-09-21 20:56:28
from django.db import models
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from django.urls import path
import hashlib
import hmac

"""
A Django app for calculating hash values.
"""


class HashTool(models.Model):
    """
    A model to hold hash calculations.
    It is not used in this implementation, but it's a placeholder
    for future enhancements.
    """
    pass


class HashView(View):
    """
    A view for calculating hash values.
    """
    
    @method_decorator(require_http_methods(['GET', 'POST']), name='dispatch')
    def get(self, request, *args, **kwargs):
        """
        Provides a GET endpoint for the hash calculation tool.
        """
        return JsonResponse({'message': 'Use POST method with data to calculate hash.'})
    
    @method_decorator(require_http_methods(['GET', 'POST']), name='dispatch')
    def post(self, request, *args, **kwargs):
        """
        Handles the POST request to calculate hash values.
        """
        try:
            data = request.POST.get('data')
            if not data:
                return JsonResponse({'error': 'No data provided.'}, status=400)

            # Calculate hash using SHA256
            hash_value = hashlib.sha256(data.encode()).hexdigest()

            # Optionally, calculate HMAC using a secret key
            # hmac_value = hmac.new(b'secret_key', data.encode(), hashlib.sha256).hexdigest()

            return JsonResponse({'hash_value': hash_value})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


def hash_tool_urls():
    """
    A function to return the URL patterns for the hash tool app.
    """
    return [
        path('hash/', HashView.as_view(), name='hash_tool'),
    ]
