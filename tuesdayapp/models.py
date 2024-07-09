from django.db import models
from django.contrib.auth.models import AbstractUser

# to store the user data(registration data)
class CustomUser(AbstractUser):
    name = models.CharField(max_length=100)

    # Remove the custom related_name and use the default ones
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='customuser_set',
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='customuser_set',
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )
class Profile(models.Model):
    user = models.OneToOneField(CustomUser , on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)




# Employer_Profile details

class Employer_Profile(models.Model):
    employer_id = models.AutoField(primary_key=True)
    employer_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=30)
    #federal_employer_identification_number = models.CharField(max_length=50)
    street_name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    number_of_employees = models.IntegerField()
    department = models.CharField(max_length=50)
    location = models.CharField(max_length=50)

    def __str__(self):
        return self.employer_name

#
class Employee_Details(models.Model):
    emp_code=models.CharField(max_length=20,primary_key=True, unique=True)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)     #added later on to fetch the email via empcode
    emp_role = models.CharField(max_length=50)
    emp_address =models.CharField(max_length=100)
    working_status = models.CharField(max_length=25)
    cont_no = models.CharField(max_length=12, unique=True)
