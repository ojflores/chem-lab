from django.conf.urls import url
from api import views


urlpatterns = [
    url(r'^course$', views.CourseLCView.as_view(), name='course-lc'),
    url(r'^course/(?P<pk>\d+)$', views.CourseRUDView.as_view(), name='course-rud'),
    url(r'^labgroup$', views.LabGroupLCView.as_view(), name='labgroup-lc'),
    url(r'^labgroup/(?P<pk>\d+)$', views.LabGroupRUDView.as_view(), name='labgroup-rud'),
    url(r'^enroll$', views.EnrollView.as_view(), name='enroll'),
]

