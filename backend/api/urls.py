from django.urls import include, path, re_path
from rest_framework import routers

from api.views import (
    TokenDestroyShemaView,
    TokenCreateShemaView,
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
    ('measure', MeasureViewSet,),
    ('orders', OrderViewSet,),
    ('ratings', RatingViewSet,),
    ('services', ServiceViewSet),
    ('types', CleaningTypeViewSet,),
    ('users', UserViewSet,),
)
for api_path in ROUTER_DATA:
    router.register(*api_path)

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'auth/token/login/?$',
            TokenCreateShemaView.as_view(), name='login'),
    re_path(r'auth/token/logout/?$',
            TokenDestroyShemaView.as_view(), name='logout'),
]
