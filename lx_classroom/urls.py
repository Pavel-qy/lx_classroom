from django.contrib import admin
from django.urls import path, include
from drf_spectacular import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
    path('schema/', views.SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', views.SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', views.SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
