from django.conf.urls import url
from api import views


urlpatterns = [
    url(r'^course$', views.CourseLCView.as_view(), name='course-lc'),
    url(r'^course/(?P<pk>\d+)$', views.CourseRUDView.as_view(), name='course-rud'),
    url(r'^template$', views.AssignmentTemplateLCView.as_view(), name='template-lc'),
    url(r'^template/(?P<pk>\d+)$', views.AssignmentTemplateRUDView.as_view(), name='template-rud'),
]

