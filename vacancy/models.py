from django.db import models
from myUser.models import User
# Create your models here.


class Vacancy(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    qualification = models.TextField(max_length=1000, null=True, blank=True)
    salary = models.CharField(max_length=100, null=True, blank=True)
    final_date = models.DateField()
    experience = models.TextField(max_length=1000, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.fullname} created vacancy: {self.title}'

    class Meta:
        db_table = 'Vacancy'


class Apply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.fullname} applied in vacancy: {self.vacancy.title}'

    class Meta:
        db_table = 'Apply'
        unique_together = ['user', 'vacancy']
