from django.contrib import admin
from django.urls import include, path


urlpatterns = [
<<<<<<< HEAD
    url(r'^admin/', admin.site.urls),
=======
    path('admin/', admin.site.urls),
    path('ping/', include('apps.ping.urls')),
>>>>>>> develop
]
