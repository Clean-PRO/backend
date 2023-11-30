from django.urls import include, path, re_path
from rest_framework import routers

from api.views import (
    TokenDestroySchemaView,
    TokenCreateSchemaView,
    CleaningTypeViewSet,
    MeasureViewSet,
    OrderViewSet,
    RatingViewSet,
    ServiceViewSet,
    UserViewSet,
)

app_name = 'api'

router = routers.DefaultRouter()
ROUTER_DATA = (
    ('cleaning-types', CleaningTypeViewSet, 'cleaning-types'),
    ('measure', MeasureViewSet, 'measure'),
    ('orders', OrderViewSet, 'orders'),
    ('ratings', RatingViewSet, 'ratings'),
    ('services', ServiceViewSet, 'services'),
    ('users', UserViewSet, 'users'),
)
for api_path in ROUTER_DATA:
    router.register(*api_path)

urlpatterns = [
    re_path(
        'auth/token/login/',
        TokenCreateSchemaView.as_view(),
        name='login',
    ),
    re_path(
        'auth/token/logout/',
        TokenDestroySchemaView.as_view(),
        name='logout',
    ),
    path('', include(router.urls)),
]
