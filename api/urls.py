from django.conf.urls import url
from api import views


urlpatterns = [
    url(r'^course$', views.CourseLCView.as_view(), name='course-lc'),
    url(r'^course/(?P<pk>\d+)$', views.CourseRUDView.as_view(), name='course-rud'),
    url(r'^group$', views.LabGroupLCView.as_view(), name='lab-group-lc'),
    url(r'^group/(?P<pk>\d+)$', views.LabGroupRUDView.as_view(), name='lab-group-rud'),
]

