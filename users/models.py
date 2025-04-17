from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, default='')
    gender = models.CharField(max_length=1, choices=[('M', 'Мужской'), ('F', 'Женский')], blank=True, default='')
    profile_photo = models.ImageField(upload_to='users_images', null=True, blank=True)
    technology_stack = models.TextField(blank=True, default='')
    group = models.CharField(max_length=10, blank=True, default='')
    course = models.IntegerField(choices=[(1, '1 курс'), (2, '2 курс'), (3, '3 курс'), (4, '4 курс')], null=True, blank=True)
    student_number = models.CharField(max_length=20, blank=True, default='')

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def set_full_name(self, full_name):
        name_parts = full_name.split()
        if len(name_parts) >= 2:
            self.first_name = name_parts[0]
            self.last_name = ' '.join(name_parts[1:])


