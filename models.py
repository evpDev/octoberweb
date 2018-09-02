from django.db import models
from django.db.models import Count, Max
from django.db.models import F


class CountryQuerySet(models.query.QuerySet):
    def with_num_cities(self):
        return self.annotate(num_cities=Count('cities__country'))

    def with_biggest_city_size(self):
        return self.annotate(biggest_city_size=Max('cities__area'))


class CountryManager(models.Manager):
    def get_queryset(self):
        return CountryQuerySet(self.model, using=self._db)

    def with_num_cities(self):
        return self.get_queryset().with_num_cities()

    def with_biggest_city_size(self):
        return self.get_queryset().with_biggest_city_size()


class Country(models.Model):
    name = models.CharField(max_length=255)
    objects = CountryManager()
    def __str__(self):
        return self.name


class CityQuerySet(models.query.QuerySet):
    def with_dencity(self):
        return self.annotate(dencity=F('population')/F('area'))


class CityManager(models.Manager):
    def get_queryset(self):
        return CityQuerySet(self.model, using=self._db)

    def with_dencity(self):
        return self.get_queryset().with_dencity()


class City(models.Model):
    country = models.ForeignKey(
        Country,
        verbose_name='Страна',
        related_name='cities',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    population = models.FloatField()
    area = models.FloatField()
    objects = CityManager()

    def __str__(self):
        return self.name
