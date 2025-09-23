from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuration Swagger/OpenAPI
schema_view = get_schema_view(
   openapi.Info(
      title="Suggestion Box API",
      default_version='v1',
      description="API pour système de boîte à suggestions avec support anonyme",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="admin@suggestion-box.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Admin Django
    path('admin/', admin.site.urls),
    
    path('api/v1/accounts/', include('accounts.urls')),

    
    # API endpoints
    path('api/v1/', include('suggestionboxapp.urls')),
    
    # Authentification DRF
    path('api/v1/auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    # Documentation API
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]

# Servir les fichiers media en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)