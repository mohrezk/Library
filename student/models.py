from django.db import models
from django.contrib.auth.models import AbstractUser
import random
# Create your models here.

class Student(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    
    username = models.CharField(max_length=30, unique=True)
    
    email = models.EmailField(unique=True)

    student_id = models.CharField(max_length=8, unique=True)

    def __str__(self):
        return f"{self.username}"


    def save(self, *args, **kwargs):
        if not self.student_id:
            self.student_id = ''.join(str(random.randint(0, 9)) for _ in range(8))
        super().save(*args, **kwargs)