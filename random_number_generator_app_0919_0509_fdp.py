# 代码生成时间: 2025-09-19 05:09:42
{
    "models.py": """
    # models.py
    from django.db import models
    """
    # 无需模型，因为我们不需要存储数据
    """
    
    views.py": """
    # views.py
    from django.http import JsonResponse
    from django.views.decorators.http import require_http_methods
    from django.views.decorators.csrf import csrf_exempt
    import random
    
    def generate_random_number(request):
        """
        View function to generate a random number and return it in JSON format.
        
        :param request: HttpRequest object
        :return: JsonResponse containing the random number
        """
        if request.method == 'GET':
            try:
                # Generate a random number between 1 and 100
                random_number = random.randint(1, 100)
                return JsonResponse({'random_number': random_number})
            except Exception as e:
                # Handle unexpected errors
                return JsonResponse({'error': 'An error occurred while generating the random number.'}, status=500)

    @csrf_exempt
    @require_http_methods(['GET'])
    def generate_random_number_view(request):
        """
        The actual view function that will be called.
        """
        return generate_random_number(request)
    """
    
    