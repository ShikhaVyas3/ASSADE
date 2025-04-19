from django.db import models

from django.db import models

class Medication(models.Model):
    medication = models.TextField()
    description = models.TextField()
    high_low_mid_use = models.IntegerField()
    num_units_per_month = models.IntegerField()
    num_units_in_stock = models.IntegerField()
    date_of_last_restock = models.DateField()

    def __str__(self):
        return f"{self.medication} - {self.description}"

class Employee(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    first_names = models.TextField()
    apellido_paterno = models.TextField(null=True, blank=True)
    appelido_materno = models.TextField(null=True, blank=True)
    privlages = models.TextField(null=True, blank=True)
    job_description = models.TextField(null=True, blank=True)
    fecha_de_nacimiento = models.DateField()
    date_added = models.DateField()

    def __str__(self):
        return self.username

class Patient(models.Model):
    first_names = models.TextField()
    apellido_paterno = models.TextField(null=True, blank=True)
    appellido_materno = models.TextField(null=True, blank=True)
    fecha_de_nacimiento = models.DateField()
    doctor = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.first_names} {self.apellido_paterno or ''} {self.appellido_materno or ''}".strip()

class Transaction(models.Model):
    med_name = models.TextField()
    med_description = models.TextField()
    emp_name = models.TextField()
    to_whom = models.TextField()
    ammount = models.IntegerField()
    restock = models.TextField()
    date_change = models.DateField()

    def __str__(self):
        return f"{self.date_change} - {self.med_name} ({self.ammount})"

