from django.db import models

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class CarModel(models.Model):
    TYPE_CHOICES = [('Sedan', 'Sedan'), ('SUV', 'SUV'), ('Wagon', 'Wagon')]
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='SUV')
    year = models.IntegerField()

    def __str__(self):
        return f"{self.car_make.name} {self.name}"
