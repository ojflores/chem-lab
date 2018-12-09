from django.contrib import admin
from django.urls import include, re_path

from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^auth/', include(('register.urls', 'register'), namespace='register')),
    re_path(r'^auth/', obtain_jwt_token),
    re_path(r'^', include(('api.urls', 'api'), namespace='api')),
]
