from django.conf.urls import url
from api import views


urlpatterns = [
    url(r'^course$', views.CourseLCView.as_view(), name='course-lc'),
    url(r'^course/(?P<pk>\d+)$', views.CourseRUDView.as_view(), name='course-rud'),
    url(r'^course$', views.LabGroupLCView.as_view(), name='labgroup-lc'),
    url(r'^course/(?P<pk>\d+)$', views.LabGroupRUDViews.as_view(), name='labgroup-rud'),
]

