from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, View
from .form import BuildingNameForm, DrawingForm, UploadDrawingForm, ProjectForm, DrawingsSearchForm
from django.http import HttpResponseRedirect
from .models import DrawingFile, Drawing, BuildingName, Project
from .drawingsnamechecker import drawings_name_checker, files_checker
from datetime import datetime
from django.db.models.functions import Concat
from django.db.models import CharField, Value as V
from django.core.exceptions import ValidationError
# Create your views here.


class NewDrawing(CreateView):
    form_class = DrawingForm
    template_name = 'drawingdoc/newbuildingname.html'
    success_url = '/'


class NewBuildingName(CreateView):
    form_class = BuildingNameForm
    template_name = 'drawingdoc/newbuildingname.html'
    success_url = '/'


class NewProjectView(CreateView):
    form_class = ProjectForm
    template_name = 'drawingdoc/newbuildingname.html'
    success_url = '/'




class UploadDrawingView(View):
    form_class = UploadDrawingForm
    template_name = 'drawingdoc/uploaddrawing.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        print(kwargs,'________E___')
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('file_field')
            list_of_errors=files_checker(files,kwargs['pk_p'])
            if not list_of_errors:
                for file in files:
                    drawing_data = drawings_name_checker(file.name)
                    drawing_file = DrawingFile(file_field=file)
                    project = Project.objects.get(id=kwargs['pk_p'])
                    building_name=BuildingName.objects.filter(abbreviation=drawing_data['building_name']).first()
                    drawing = Drawing(
                        design_stage=drawing_data['design_stage'],
                        branch=drawing_data['branch'],
                        date_drawing=drawing_data['date_drawing'],
                        date_update=datetime.now(),
                        draw_number=drawing_data['draw_number'],
                        draw_title=drawing_data['draw_title'],
                        building_name=building_name,
                        revision=drawing_data['revision'],
                        file=drawing_file,
                        project=project,
                    )
                    drawing_file.save()
                    drawing.save()
                    return HttpResponseRedirect('/success/')
            for error in list_of_errors:
                form.add_error('file_field', error)
            form.add_error('file_field', 'No file has been saved, please correct the above errors')
            form.clean()
            return render(request, self.template_name, {'form': form})
        return render(request, self.template_name, {'form': form})



class DrawingsListView(View):
    template_name = 'drawingdoc/drawings_list.html'

    def get(self, request, *args, **kwargs):
        revision_list = []
        object_dict = {}
        revision_date_list = []
        drawing_number_list=[]
        form = DrawingsSearchForm(request.GET)
        if form.is_valid():
            design_stage = form.cleaned_data.get('design_stage', '').strip()
            draw_number = form.cleaned_data.get('draw_number', '').strip()
            date_from = form.cleaned_data.get('date_from', '')
            date_to = form.cleaned_data.get('date_to', '')
            branch = form.cleaned_data.get('branch', '').strip()
            building_name_id = [x.id for x in form.cleaned_data.get('building_name', '')]
            queryset = Drawing.objects.filter(project=Project.objects.get(id=kwargs['pk_p']),design_stage=design_stage, building_name__in=building_name_id, branch=branch)
            if draw_number:
                queryset = queryset.filter(draw_number__icontains=draw_number)
            if date_from and date_to:
                queryset = queryset.filter(date_drawing__gte=date_from).filter(date_drawing__lte=date_to)
            elif date_from:
                queryset = queryset.filter(date_drawing__gte=date_from)
            elif date_to:
                queryset = queryset.filter(date_drawing__lte=date_to)

            queryset_rev_numb=queryset.values_list('revision', 'draw_number')
            for rev_numb in queryset_rev_numb:
                if rev_numb[0] not in revision_list:
                    revision_list.append(rev_numb[0])
                if rev_numb[1] not in drawing_number_list:
                    drawing_number_list.append(rev_numb[1])

            for dr_number in drawing_number_list:
                object_dict[dr_number] = {
                    'obj': queryset.filter(draw_number=dr_number).values('design_stage','branch','date_drawing','draw_number', 'draw_title', 'building_name', 'revision').first(),
                    'rev_date': queryset.filter(draw_number=dr_number).values('revision','date_drawing'),
                }

        return render(request, self.template_name,
                      {
                          'form': form,
                          'object_dict':object_dict,
                          'revision_list': revision_list,
                       })