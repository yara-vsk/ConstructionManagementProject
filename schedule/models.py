from django.db import models
from drawingdoc.models import Project


class Schedule(models.Model):
    old_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=250, blank=True)
    date_start = models.DateField()
    date_finish = models.DateField()
    predecessors = models.CharField(max_length=100, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    outline_level = models.IntegerField()
    progress = models.IntegerField(default=0)

    def __str__(self):
        return self.name