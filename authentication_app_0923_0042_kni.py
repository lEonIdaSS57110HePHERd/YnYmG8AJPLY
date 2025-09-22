# 代码生成时间: 2025-09-23 00:42:40
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
import json

"""
Authentication app for handling user login.
"""

class AuthenticationView:
    """
    A class-based view for handling user authentication.
    """
    @method_decorator(csrf_exempt, name='dispatch')
    @require_http_methods(['POST'])
    def post(self, request):
        """
        Authenticate a user and log them in if credentials are correct.
        """
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            if not username or not password:
                raise ValidationError('Both username and password are required')
            user = authenticate(request, username=username, password=password)
            if user is None:
                return JsonResponse({'error': 'Invalid username or password'}, status=401)
            login(request, user)
            return JsonResponse({'message': 'User authenticated and logged in successfully'}, status=200)
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'An error occurred during authentication'}, status=500)

"""
URL configuration for the authentication app.
"""
from django.urls import path
from .views import AuthenticationView

urlpatterns = [
    path('login/', AuthenticationView.as_view(), name='user_login'),
]
