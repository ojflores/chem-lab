from django.contrib.auth import get_user_model
from django.db import models


class Instructor(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    wwuid = models.CharField(max_length=7)

class Course(models.Model):
    name = models.CharField(max_length=100)

class LabGroup(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)

class Student(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    lab_group = models.ForeignKey(LabGroup, on_delete=models.CASCADE)
    wwuid = models.CharField(max_length=7)

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

class Assignment(models.Model):
    assignment_template = models.ForeignKey(AssignmentTemplate, on_delete=models.CASCADE)
    lab_group = models.ForeignKey(LabGroup, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

class AssignmentEntry(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    completed = models.BooleanField()
    grade = models.FloatField()

class TaskEntry(models.Model):
    assignment_entry = models.ForeignKey(AssignmentEntry, on_delete=models.CASCADE)
    task_template = models.ForeignKey(TaskTemplate, on_delete=models.CASCADE)
    attempts = models.IntegerField()
    passed = models.BooleanField()

