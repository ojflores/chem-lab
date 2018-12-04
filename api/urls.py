from django.conf.urls import url
from api import views


urlpatterns = [
    url(r'^assignment$', views.AssignmentLCView.as_view(), name='assignment-lc'),
    url(r'^assignment/(?P<pk>\d+)$', views.AssignmentRUDView.as_view(), name='assignment-rud'),
    url(r'^assignment/(?P<assignment>\d+)/entry$', views.AssignmentEntryView.as_view(), name='assignment-entry'),
    url(r'^assignment/(?P<assignment>\d+)/start$', views.AssignmentEntryStartView.as_view(), name='assignment-entry-start'),
    url(r'^assignment/(?P<assignment>\d+)/submit$', views.AssignmentEntrySubmitView.as_view(), name='assignment-entry-submit'),
    url(r'^course$', views.CourseLCView.as_view(), name='course-lc'),
    url(r'^course/(?P<pk>\d+)$', views.CourseRUDView.as_view(), name='course-rud'),
    url(r'^enroll$', views.EnrollView.as_view(), name='enroll'),
    url(r'^instructor$', views.InstructorLCView.as_view(), name='instructor-lc'),
    url(r'^instructor/(?P<pk>\d+)$', views.InstructorRUDView.as_view(), name='instructor-rud'),
    url(r'^labgroup$', views.LabGroupLCView.as_view(), name='lab-group-lc'),
    url(r'^labgroup/(?P<pk>\d+)$', views.LabGroupRUDView.as_view(), name='lab-group-rud'),
    url(r'^student$', views.StudentLCView.as_view(), name='student-lc'),
    url(r'^student/(?P<pk>\d+)$', views.StudentRUDView.as_view(), name='student-rud'),
    url(r'^template$', views.AssignmentTemplateLCView.as_view(), name='template-lc'),
    url(r'^template/(?P<pk>\d+)$', views.AssignmentTemplateRUDView.as_view(), name='template-rud'),
]

