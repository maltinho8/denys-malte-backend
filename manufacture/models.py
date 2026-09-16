from django.db import models

class CountryChoices(models.TextChoices):
    GERMANY = "germany", "Germany",
    JAPAN = "japan", "Japan",

class CarTypeChoices(models.TextChoices):
    CABRIOLET = "cabriolet", "Cabriolet",
    SUV = "suv", "SUV",
    FOUR_DOOR = "four_door", "Four Door",
    HATCHBACK = "hatchback", "Hatchback",
    COUPE = "coupe", "Coupe",

class ProductionStatusChoices(models.TextChoices):
    ACTIVE = "active", "Active",
    PAUSED = "paused", "Paused",
    DISCONTINUED = "discontinued", "Discontinued",

# Model for car manufacturers
class Manufacture(models.Model):
    name = models.CharField(max_length=100, null=False)
    country = models.CharField(choices=CountryChoices.choices, max_length=100)
    car_type = models.CharField(choices=CarTypeChoices.choices, max_length=100, null=True, blank=True)
    production_status = models.CharField(choices=ProductionStatusChoices.choices, max_length=20, default=ProductionStatusChoices.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.country}"

    class Meta:
        verbose_name = "Manufacture"
        verbose_name_plural = "Manufactures"
        ordering = ["created_at"]