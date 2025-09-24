# 代码生成时间: 2025-09-24 14:40:26
from django.db import models
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import path
from django.views import View
from urllib.parse import urlparse
import requests

# models.py
class UrlLink(models.Model):
    """Model to store URL that needs to be validated."""
    url = models.URLField(unique=True)
    validated = models.BooleanField(default=False)
    validation_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.url

# views.py
class ValidateUrlView(View):
    """View to validate a URL."""
    def post(self, request):
        """Handle POST request to validate a URL."""
        url = request.POST.get('url')
        if not url:
            return JsonResponse({'error': 'URL is required.'}, status=400)

        try:
            result = validate_url(url)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        return JsonResponse({'url': url, 'is_valid': result['is_valid'], 'message': result['message']}, status=200)

    def get(self, request):
        """Handle GET request to show form for URL validation."""
        return render(request, 'url_validator/form.html')

def validate_url(url):
    """Function to validate the URL."""
    parsed_url = urlparse(url)
    if not parsed_url.scheme or not parsed_url.netloc:
        return {'is_valid': False, 'message': 'Invalid URL format.'}
    try:
        response = requests.head(url)
        if response.status_code == 200:
            return {'is_valid': True, 'message': 'URL is valid.'}
        else:
            return {'is_valid': False, 'message': f'URL returned status code {response.status_code}.'}
    except requests.RequestException as e:
        return {'is_valid': False, 'message': str(e)}

# urls.py
urlpatterns = [
    path('validate/', ValidateUrlView.as_view(), name='validate_url'),
]

# templates/url_validator/form.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>URL Validator</title>
</head>
<body>
    <h1>URL Validator</h1>
    <form action="{% url 'validate_url' %}" method="post">
        {% csrf_token %}
        <label for="url">Enter URL:</label>
        <input type="text" id="url" name="url" required>
        <button type="submit">Validate</button>
    </form>
</body>
</html>