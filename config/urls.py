from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # URLs do app de login
    path('', include('portal.urls')),            # URLs do app principal
]