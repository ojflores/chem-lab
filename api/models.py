from django.contrib.auth import get_user_model
from django.db import models


class Student(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    wwuid = models.CharField(max_length=7)

class Instructor(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    wwuid = models.CharField(max_length=7)

class Course(models.Model):
    name = models.CharFeild(max_length=100)

class LabGroup(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)

class AssignmentTemplate(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class TaskTemplate(models.Model):
    assignment_template = models.ForeignKey(AssignmentTemplate, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image_urls = models.TextField()
    acceptable_inputs = models.TextField()
    accuracy_check = models.BooleanField()
    accuracy = models.IntegerField()
    multiple_choice = models.BooleanField()  # needs implementation
    attempts_allowed = models.IntegerField()
    keyword_check = models.BooleanField()
    keywork_list = models.TextField()
    keyword_min = models.IntegerField()
    points = models.FloatField()

class AssignmentEntry(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment_template = models.ForeignKey(AssignmentTemplate, on_delete=models.CASCADE)
    grade = models.floatField()

class TaskEntry(models.Model):
    assignment_entry = models.ForeignKey(AssignmentEntry, on_delete=models.CASCADE)
    task_template = models.ForeignKey(TaskTemplate, on_delete=models.CASCADE)
    attempts = models.IntegerField()
    completed = models.BooleanField()
    passed = models.BooleanField()

