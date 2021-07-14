from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone



class User(AbstractUser):
    pass


class Country(models.Model): # Only admins can add country
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=3)
    low_image = models.URLField() # Lower resolution image
    high_image = models.URLField(null=True) # Higher resolution image

    def __getattribute__(self, name):
        attr = models.Model.__getattribute__(self, name)
        if name == 'low_image' and not attr:
            return 'https://www.rdasia.com/wp-content/uploads/sites/2/2020/01/00-aeroplane-facts-shutterstock_112931425-770.jpg'
        return attr

    def __str__(self):
        return f'{self.name} ({self.code})'


class Trip(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    days = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(60)])
    private = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)
    clonedFrom = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='cloned')

    def __str__(self):
        return f'{self.owner} {self.country} {self.days}days'

    def default_owner(self):
        return self.owner if not self.clonedFrom else self.clonedFrom


class Destination(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


class TripDetail(models.Model):
    class Meta:
        unique_together = (('trip', 'day'),)

    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="tripDetail")
    # 1st day, 2nd day, 3rd day, etc.
    day = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(60)])

    def __str__(self):
        return f'TripID{self.trip.id} - Day{self.day}'


class TripDetailDestination(models.Model):
    class Meta:
        unique_together = (('tripDetail', 'destination'),)

    tripDetail = models.ForeignKey(TripDetail, on_delete=models.CASCADE, related_name="destinations")
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    # Duration in hours
    duration = models.DecimalField(null=True, max_digits=3, decimal_places=1, validators=[MinValueValidator(0.1), MaxValueValidator(24)])

    def __str__(self):
        return f'TripDetail ID{self.tripDetail.id} - {self.destination} ({self.duration}hours)'
    