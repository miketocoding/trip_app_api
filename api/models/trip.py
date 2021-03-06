from django.db import models
from django.contrib.auth import get_user_model

# import validator
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here
class Trip(models.Model):
    # define fields
    image = models.CharField(max_length=255)
    location = models.CharField(max_length=100)
    start = models.DateField()
    end = models.DateField()
    travelers = models.CharField(max_length=255)
    rating = models.PositiveIntegerField(
    default=5, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    standouts = models.TextField()

    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )

    def __str__(self):
        # This must return a string
        return f"Trip to {self.location}."

    def as_dict(self):
        """Returns dictionary version of Mango models"""
        return {
            'id': self.id,
            'location': self.location,
            'start': self.start,
            'end': self.end,
            'travelers': self.travelers,
            'rating': self.rating,
            'standouts': self.standouts
        }
