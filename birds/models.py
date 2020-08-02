from django.core.validators import MinValueValidator
from django.db import models


class Birds(models.Model):
    class Species(models.TextChoices):
        CROW = 'crow'
        MAGPIE = 'magpie'
        PIGEON = 'pigeon'
        SPARROW = 'sparrow'
        TITMOUSE = 'titmouse'

    class Color(models.TextChoices):
        BLACK = 'black'
        WHITE = 'white'
        BLACK_WHITE = 'black & white'
        GREY = 'grey'
        RED = 'red'
        RED_WHITE = 'red & white'

    species = models.CharField(
        choices=Species.choices,
        max_length=255
    )
    name = models.CharField(
        primary_key=True,
        max_length=255
    )
    color = models.CharField(
        choices=Color.choices,
        max_length=255
    )
    body_length = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    wingspan = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        managed = False
        db_table = 'birds'

    def __str__(self):
        return '{} (species: {}, color: {}, body length: {}, wingspan: {})'.format(self.name, self.species, self.color, self.body_length, self.wingspan)


