from django.conf.urls import url
from api import views


urlpatterns = [
    url(r'^course$', views.CourseLCView.as_view(), name='course-lc'),
    url(r'^course/(?P<pk>\d+)$', views.CourseRUDView.as_view(), name='course-rud'),

    url(r'^instructor$', views.InstructorLCView.as_view(), name='instructor-lc'),
    url(r'^instructor/(?P<pk>\d+)$', views.InstructorRUDView.as_view(), name='instructor-rud'),
]

