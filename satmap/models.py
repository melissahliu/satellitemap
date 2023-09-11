import ee
import folium

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import ArrayField

from .utils import initialize_gee

from location_field.models.plain import PlainLocationField

class Layer(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    band = models.CharField(max_length=255)
    min = models.DecimalField(max_digits=10,
        decimal_places=3, blank=True, null=True)
    max = models.DecimalField(max_digits=10,
        decimal_places=3, blank=True, null=True)
    opacity = models.DecimalField(max_digits=3, decimal_places=2, default=0.5, validators=[
            MinValueValidator(0),
            MaxValueValidator(1)])
    #palette = ArrayField(models.CharField(max_length=255), default=['blue', 'purple', 'cyan', 'green', 'yellow', 'red'])
    palette = models.TextField(default = "[ 'blue', 'purple', 'cyan', 'green', 'yellow', 'red' ]")
    units = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    is_collection = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def get_array_params(self):
        params = {}
        for field in ['min', 'max','opacity']:
            if getattr(self, field):
                params[field] = float(getattr(self,field))
        params['dimensions'] = '400x400'
        return params

    def get_vis_params(self):
        params = {}
        for field in ['min', 'max','opacity']:
            if getattr(self, field):
                params[field] = float(getattr(self,field))
        if self.palette:
            params['palette'] = self.get_palette_list()
        return params

    def __str__(self):
        return self.name
    
    def get_palette_list(self):
        palette = self.palette.split(', ')
        palettelist = []
        for color in palette:
            palettelist.append(color[7:-5])
        return palettelist

class Project(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=17, decimal_places=14, blank=True)
    longitude = models.DecimalField(max_digits=17, decimal_places=14, blank=True)
    location = PlainLocationField(based_fields=['city'], zoom=7)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    datasets = models.ManyToManyField(Layer, blank=True)

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'pk':self.id})
    
    def save(self, *args, **kwargs):
        if not self.latitude:
            self.latitude, self.longitude = self.location.split(',')
        for map in self.map_set.all():
            for layer in self.datasets.all():
                map.layer.add(layer)
            map.save()
        super(Project, self).save(*args, **kwargs)

class Rectangle(models.Model):
    southwest = models.DecimalField(max_digits=9, decimal_places=6)

class Map(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, 
        blank=True, null=True)
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=17, decimal_places=14, blank=True)
    longitude = models.DecimalField(max_digits=17, decimal_places=14, blank=True)
    location = PlainLocationField(based_fields=['city'], zoom=7)
    zoom = models.IntegerField(default=8)
    layer = models.ManyToManyField(Layer, blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['title']
    
    def save(self, *args, **kwargs):
        if not self.latitude:
            self.latitude, self.longitude = self.location.split(',')
        super(Map, self).save(*args, **kwargs)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        if self.project:
            return self.title + ' (' + self.project.name + ')'
        else:
            return self.title
    
    def duplicate(self, project):
        map = Map.objects.create(
            project = project,
            title = self.title,
            description = self.description,
            location = self.location,
            zoom = self.zoom,
            start_date = self.start_date,
            end_date = self.end_date,
            published_date = self.published_date
        )
        map.layer.set(self.layer.all())

    def get_array(self):
        initialize_gee()


class MapRender(models.Model):
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    html = models.TextField(blank=True)
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        if self.date:
            return '{}: {}'.format(self.map.title, self.date)
