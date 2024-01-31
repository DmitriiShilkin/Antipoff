"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers, permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from service.views import QueryViewSet, ResultViewSet, HistoryViewSet, PingView, index_view, ExternalServerEmulatorView

router = routers.DefaultRouter()

router.register('query', QueryViewSet, basename='query')
router.register('result', ResultViewSet, basename='result')
router.register('history', HistoryViewSet, basename='history')

# Автодокументация swagger и redoc
schema_view = get_schema_view(
   openapi.Info(
      title="Service API",
      default_version='v1',
      description="Antipoff test task",
      terms_of_service="https://www.google.com/policies/terms/",
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny, ],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='index'),
    path('api/v1/', include(router.urls)),
    path('api/v1/emulate-external-server/', ExternalServerEmulatorView.as_view(), name='emulate-external-server'),
    path('api/v1/ping/', PingView.as_view(), name='ping'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^swagger?(\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
