from django.db import models
# Create your models here.

ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('user', 'User'),
)

STATUS_CHOICES = (
    ('active', 'Active'),
    ('inactive', 'Inactive'),
)

class User(models.Model):
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return self.username  

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=10, unique=True)
    department = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=15)
    admission_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    cpf = models.CharField(max_length=11, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.user.username