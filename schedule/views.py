import json

from django.db.models.functions import Concat, Extract, Trunc

from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views import View
from django.db.models import CharField, Value as V, DateTimeField, DateField

from drawingdoc.custommixins import CustomPermMixin
from drawingdoc.models import Project
from drawingdoc.utils import menu
from schedule.form import UploadScheduleForm
import pandas

from schedule.models import Schedule
from schedule.serializers import ScheduleSerializer, ScheduleExportSerializer


class UploadCsvView(CustomPermMixin, View):
    form_class = UploadScheduleForm
    template_name = 'drawingdoc/uploaddrawing.html'
    permission_required = 'schedule.add_schedule'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        project = get_object_or_404(Project, pk=kwargs['pk_p'])
        return render(request, self.template_name, {'form': form,
                                                    'menu': menu,
                                                    'project': project})

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs['pk_p'])
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            csv = pandas.read_csv(request.FILES['file_csv'])
            schedule_dicts = csv.to_dict(orient="index")
            for dict_s in schedule_dicts.values():
                dict_s['project'] = project.id
            serializer = ScheduleSerializer(data=list(schedule_dicts.values()), many=True)
            print(list(schedule_dicts.values())[0])
            if serializer.is_valid():
                serializer.save()
                return render(request, self.template_name, {'form': form,
                                                            'menu': menu,
                                                            'project': project})
        return render(request, self.template_name, {'form': form,
                                                    'menu': menu,
                                                    'project': project})


class ScheduleView(CustomPermMixin, View):
    template_name = 'schedule/schedule_view.html'
    permission_required = 'schedule.view_schedule'

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs['pk_p'])
        tasks = Schedule.objects.annotate(start=Trunc('date_start','day',output_field=DateField()),
                                          end=Trunc('date_finish','day',output_field=DateField()),
                                          _id=Concat(V('ask '), 'id',output_field=CharField()),
                                          ).values('start', 'end', '_id', 'name'
                                                   ).annotate(id=Concat(V('T'),"_id",output_field=CharField())
                                                              ).values('start', 'end', 'id', 'name')
        serializer = ScheduleExportSerializer(tasks, many=True)
        return render(request, self.template_name, {'menu': menu,
                                                    'project': project,
                                                    'tasks': json.dumps(serializer.data)})

