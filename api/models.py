from django.contrib.auth import get_user_model
from django.db import models


class Student(models.Model)
    wwuid = models.CharField(max_length=7)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
