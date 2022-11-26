from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, View
from .form import BuildingNameForm, DrawingForm, UploadDrawingForm, ProjectForm
from django.http import HttpResponseRedirect
from .models import DrawingFile, Drawing, BuildingName, Project
from .drawingsnamechecker import drawings_name_checker
from datetime import datetime
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


def upload_drawing(request):
    if request.method == "POST":
        uploaded_file = request.FILES['drawing']
        print(uploaded_file.name)
    return render(request, 'drawingdoc/uploaddrawing.html')


class UploadDrawingView(View):
    form_class = UploadDrawingForm
    template_name = 'drawingdoc/uploaddrawing.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('file_field')
            for file in files:
                print(file.name)
                drawing_data = drawings_name_checker(file.name)
                if drawing_data:
                    print('yessssss')
                    drawing_file = DrawingFile(file_field=file)
                    try:
                        project=Project.objects.get(abbreviation=drawing_data['project'])
                        building_name=BuildingName.objects.get(abbreviation=drawing_data['building_name'])
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
                    except:
                        form.add_error('file_field','Please send the file with the correct name')
                        form.clean()
                        return render(request, self.template_name, {'form': form})
            return HttpResponseRedirect('/success/')

        return render(request, self.template_name, {'form': form})