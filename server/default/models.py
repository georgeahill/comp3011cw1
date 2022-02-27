from django.db import models
from django.contrib.auth.models import User


class Module(models.Model):
    code = models.CharField(primary_key=True, unique=True, max_length=3)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Professor(models.Model):
    code = models.CharField(primary_key=True, unique=True, max_length=4)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name[0]}. {self.last_name} ({self.code})"


class Teaching(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    semester = models.IntegerField(choices=[(1, 1), (2, 2)])
    year = models.IntegerField()

    def __str__(self):
        return f"{self.professor} teaching {self.module} in semester {self.semester} of {self.year}"

    class Meta:
        unique_together = ("professor", "module", "semester", "year")


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rated = models.ForeignKey(Teaching, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=((1, 1), (2, 2), (3, 3), (4, 4), (5, 5)))

    class Meta:
        unique_together = ("user", "rated")
