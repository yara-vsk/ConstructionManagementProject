from rest_framework import serializers

from drawingdoc.models import Project
from .models import Schedule


class ScheduleSerializer(serializers.Serializer):

    ID = serializers.IntegerField()
    Name = serializers.CharField(max_length=250)
    Start = serializers.DateField(format="%d-%m-%Y", input_formats=['%a %m/%d/%y', 'iso-8601'])
    Finish = serializers.DateField(format="%d-%m-%Y", input_formats=['%a %m/%d/%y', 'iso-8601'])
    Predecessors = serializers.CharField(max_length=100)
    project = serializers.IntegerField()

    def create(self, validated_data):
        return Schedule.objects.create(
            old_id=validated_data['ID'],
            name = validated_data['Name'],
            date_start = validated_data['Start'],
            date_finish = validated_data['Finish'],
            predecessors = validated_data['Predecessors'],
            project = Project.objects.get(id=validated_data['project'])
        )


class ScheduleExportSerializer(serializers.Serializer):

    id = serializers.CharField(max_length=100, read_only=True)
    name = serializers.CharField(max_length=250,read_only=True)
    start = serializers.DateField(read_only=True)
    end = serializers.DateField(read_only=True)
    progress = serializers.IntegerField(default=0, read_only=True)
    dependencies = serializers.CharField(default='Task 1',max_length=100, read_only=True)