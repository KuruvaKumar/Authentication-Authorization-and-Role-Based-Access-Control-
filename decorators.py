# authentication/decorators.py
from functools import wraps
from django.http import JsonResponse
from django.contrib.auth.models import Group

def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return JsonResponse({'message': 'User is not authenticated'}, status=403)
            if not request.user.groups.filter(name=role).exists():
                return JsonResponse({'message': 'Permission denied'}, status=403)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
