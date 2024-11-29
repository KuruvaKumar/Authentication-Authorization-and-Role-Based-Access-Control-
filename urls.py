from django.contrib import admin
from django.urls import path, include
from authentication.views import register, user_login, user_logout, admin_only_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    
]
