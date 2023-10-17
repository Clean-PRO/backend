from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path # noqa
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from drf_yasg import openapi # noqa
from drf_yasg.views import get_schema_view # noqa
from rest_framework import permissions # noqa

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='api')),
    path('spectacular/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('spectacular/docs/',
         SpectacularSwaggerView.as_view(url_name='schema'),
         name='docs',
         ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
