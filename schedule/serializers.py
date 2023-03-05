import re

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
    outline_level = serializers.IntegerField()

    def create(self, validated_data):
        return Schedule.objects.create(
            old_id=validated_data['ID'],
            name=validated_data['Name'],
            date_start=validated_data['Start'],
            date_finish=validated_data['Finish'],
            predecessors=validated_data['Predecessors'],
            project=Project.objects.get(id=validated_data['project']),
            outline_level=validated_data['outline_level'],
        )

    def validate_outline_level(self,value):
        try:
            int_value=int(value)
        except KeyError:
            raise serializers.ValidationError("Otline level must be integer type.")
        return int_value

    def validate_Predecessors(self,value):
        try:
            new_value= 'Task ' + str(int(value))
        except ValueError:
            if value == 'nan':
                return ''
            values=[]
            for value_part in value.split(';'):
                try:
                    new_value_part = 'Task ' + str(int(value_part))
                    values.append(new_value_part)
                except ValueError:
                    match = re.search(r'[A-Za-z]', value_part)
                    if match:
                        try:
                            new_value_part = 'Task ' + str(int(value_part[:match.start()]))
                            values.append(str(new_value_part))
                        except ValueError:
                            raise serializers.ValidationError("The 'predecessor' data format is not appropriate.")
                    else:
                        raise serializers.ValidationError("The 'predecessor' data format is not appropriate.")
            new_value = values[0] if len(values) == 1 else ", ".join(values)
        return new_value


class ScheduleExportSerializer(serializers.Serializer):

    id = serializers.CharField(max_length=100, read_only=True)
    name = serializers.CharField(max_length=250,read_only=True)
    start = serializers.DateField(read_only=True)
    end = serializers.DateField(read_only=True)
    progress = serializers.IntegerField(read_only=True)
    dependencies = serializers.CharField(default="Task 1", max_length=100, read_only=True)