from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

class RoleRequiredMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        required_role = view_kwargs.get('role')
        if required_role:
            if not request.user.is_authenticated:
                return JsonResponse({'message': 'User is not authenticated'}, status=403)
            if not request.user.groups.filter(name=required_role).exists():
                return JsonResponse({'message': 'Permission denied'}, status=403)
        return None
