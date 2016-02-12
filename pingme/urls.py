from django.conf.urls import url, include
from pingme import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'devices', views.DeviceViewSet)
router.register(r'locations', views.LocationViewSet)



urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-token-auth/', views.obtain_auth_token_and_user),
]