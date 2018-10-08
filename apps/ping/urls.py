from django.conf.urls import url
from apps.ping import views


urlpatterns = [
    url(r'^$', views.Ping.as_view()),
]
