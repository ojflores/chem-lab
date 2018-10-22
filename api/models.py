from django.contrib.auth import get_user_model
from django.db import models


class Instructor(models.Model):
    '''
    The Instructor model represents an instructor that can teach and manage 
    chemistry labs.
    '''
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    wwuid = models.CharField(max_length=7)

class Course(models.Model):
    '''
    The Course model represents a course such as CHEM241.
    '''
    name = models.CharField(max_length=100)

class LabGroup(models.Model):
    '''
    The LabGroup model represents a group of students in the same lab. 
    '''
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    term = models.CharField(max_length=10)

    class Meta:
        db_table = 'api_lab_group'

class Student(models.Model):
    '''
    The Student model represents a student in a chemistry class.
    '''
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    lab_group = models.ForeignKey(LabGroup, on_delete=models.CASCADE)
    wwuid = models.CharField(max_length=7)

class AssignmentTemplate(models.Model):
    '''
    The AssignmentTemplate model represents the general details of a specific 
    lab assignment.
    '''
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'api_assignment_template'

class TaskTemplate(models.Model):
    '''
    The TaskTemplate model represents the details of a specific task of an 
    assignment such as the question to ask and how to grade them.
    '''
    assignment_template = models.ForeignKey(AssignmentTemplate, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image_urls = models.TextField()
    acceptable_inputs = models.TextField()
    accuracy_check = models.BooleanField()
    accuracy = models.IntegerField()
    multiple_choice = models.BooleanField()
    multiple_choise_options = models.TextField()
    attempts_allowed = models.IntegerField()
    keyword_check = models.BooleanField()
    keywork_list = models.TextField()
    keyword_min = models.IntegerField()
    points = models.FloatField()

    class Meta:
        db_table = 'api_task_template'

class Assignment(models.Model):
    '''
    The Assignment model represents the "assignment" of an AssignmentTemplate. 
    It holds the due dates for this particular assignment.
    '''
    assignment_template = models.ForeignKey(AssignmentTemplate, on_delete=models.CASCADE)
    lab_group = models.ForeignKey(LabGroup, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

class AssignmentEntry(models.Model):
    '''
    The AssignmentEntry model represents a users attempt to complete an 
    Assignment.
    '''
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    completed = models.BooleanField()
    grade = models.FloatField()

    class Meta:
        db_table = 'api_assignment_entry'

class TaskEntry(models.Model):
    '''
    The TaskEntry model represents a users attempt to complete a task for an 
    Assignment following the TaskTemplate.
    '''
    assignment_entry = models.ForeignKey(AssignmentEntry, on_delete=models.CASCADE)
    task_template = models.ForeignKey(TaskTemplate, on_delete=models.CASCADE)
    attempts = models.IntegerField()
    passed = models.BooleanField()

    class Meta:
        db_table = 'api_task_entry'

