from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cuenta/', include('cuenta.urls')),
    path('panel/', include('panel.urls', namespace='panel')),
]