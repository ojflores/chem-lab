from django.conf.urls import url
from api import views


urlpatterns = [
    url(r'^course$', views.CourseLCView.as_view(), name='course-lc'),
    url(r'^course/(?P<pk>\d+)$', views.CourseRUDView.as_view(), name='course-rud'),
    url(r'^student$', views.StudentLCView.as_view(), name='student-lc'),
    url(r'^student/(?P<pk>\d+)$', views.StudentRUDView.as_view(), name='student-rud'),
]

