import os
from django.shortcuts import render, redirect
from django.views.generic import CreateView, View, ListView
from .form import BuildingNameForm, UploadDrawingForm, ProjectForm, DrawingsSearchForm
from django.http import HttpResponseRedirect, Http404
from .models import DrawingFile, Drawing, BuildingName, Project
from .drawingsnamechecker import drawings_name_checker
from .fileschecker import files_checker
from datetime import datetime


class ProjectListView(ListView):
    model = Project
    template_name = 'drawingdoc/projects_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list
        return super().get_context_data(
            object_list=queryset,
            **kwargs)


class ProjectInfoView(ListView):
    template_name = 'drawingdoc/project_info.html'


    def get(self, request, *args, **kwargs):
        try:
            project = Project.objects.get(id=kwargs['pk_p'])
        except Project.DoesNotExist:
            raise Http404("Project does not exist")
        building_names=BuildingName.objects.filter(project=project.id).all()
        print(building_names)
        return render(request, self.template_name, {'project': project, 'building_list':building_names})


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
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        try:
            project = Project.objects.get(id=kwargs['pk_p'])
        except Project.DoesNotExist:
            raise Http404("Project does not exist")
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('file_field')
            list_of_errors = files_checker(files, kwargs['pk_p'])
            if not list_of_errors:
                for file in files:
                    drawing_data = drawings_name_checker(file.name)
                    file_name = "_".join(file.name.split("_")[0:6])
                    drawing_file = DrawingFile(file_field=file, file_name=file_name)
                    building_name = BuildingName.objects.filter(abbreviation=drawing_data['building_name']).first()
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
        drawing_number_list = []
        form = DrawingsSearchForm(request.GET)
        try:
            project = Project.objects.get(id=kwargs['pk_p'])
        except Project.DoesNotExist:
            raise Http404("Project does not exist")
        if form.is_valid():
            design_stage = form.cleaned_data.get('design_stage', '').strip()
            draw_number = form.cleaned_data.get('draw_number', '').strip()
            date_from = form.cleaned_data.get('date_from', '')
            date_to = form.cleaned_data.get('date_to', '')
            branch = form.cleaned_data.get('branch', '').strip()
            building_name_id = [x.id for x in form.cleaned_data.get('building_name', '')]
            queryset = Drawing.objects.filter(project=project, design_stage=design_stage,
                                              building_name__in=building_name_id, branch=branch)
            if draw_number:
                queryset = queryset.filter(draw_number__icontains=draw_number)
            if date_from and date_to:
                queryset = queryset.filter(date_drawing__gte=date_from).filter(date_drawing__lte=date_to)
            elif date_from:
                queryset = queryset.filter(date_drawing__gte=date_from)
            elif date_to:
                queryset = queryset.filter(date_drawing__lte=date_to)

            queryset_rev_numb = queryset.values_list('revision', 'draw_number')
            for rev_numb in queryset_rev_numb:
                if rev_numb[0] not in revision_list:
                    revision_list.append(rev_numb[0])
                if rev_numb[1] not in drawing_number_list:
                    drawing_number_list.append(rev_numb[1])

            for dr_number in drawing_number_list:
                all_rev = []
                for revision_val in queryset.filter(draw_number=dr_number).values_list('revision'):
                    all_rev.append(revision_val[0])
                object_dict[dr_number] = {
                    'obj': queryset.filter(draw_number=dr_number).values('design_stage', 'branch', 'file__file_field',
                                                                         'date_drawing',
                                                                         'draw_number', 'draw_title', 'building_name',
                                                                         'revision').first(),
                    'rev_date': queryset.filter(draw_number=dr_number).values('revision', 'date_drawing', 'id'),
                    'all_rev': all_rev,
                }
            revision_list.sort()
        return render(request, self.template_name,
                      {
                          'form': form,
                          'object_dict': object_dict,
                          'revision_list': revision_list
                      })


class DrawingInfoView(View):
    template_name = 'drawingdoc/drawing_info.html'

    def get(self, request, *args, **kwargs):
        try:
            drawing_data = Drawing.objects.get(id=kwargs['pk'])
        except Drawing.DoesNotExist:
            raise Http404("Drawing does not exist")
        return render(request, self.template_name, {'obj': drawing_data})


class DrawingDeleteView(View):

    def get(self, request, *args, **kwargs):
        try:
            drawing= Drawing.objects.get(id=kwargs['pk'])
            file_url = str(drawing.file.file_field.path)
            drawing.file.delete()
            if os.path.isfile(file_url):
                print(file_url)
                os.remove(file_url)
        except Drawing.DoesNotExist:
            raise Http404("Drawing does not exist")
        return HttpResponseRedirect(f'/project/{kwargs["pk_p"]}/drawing_documents/list/')


class DrawingUpdateView(View):
    form_class = UploadDrawingForm
    template_name = 'drawingdoc/uploaddrawing.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('file_field')
            list_of_errors = files_checker(files, kwargs['pk_p'], update=True)
            if not list_of_errors:
                drawing_data = drawings_name_checker(files[0].name)
                drawing = Drawing.objects.get(id=kwargs['pk'])
                if drawing.project.abbreviation == drawing_data['project'] and drawing.design_stage == drawing_data[
                    'design_stage'] and drawing.branch == drawing_data['branch'] and drawing.draw_number == \
                        drawing_data['draw_number'] and drawing.revision == drawing_data[
                    'revision'] and drawing.building_name.abbreviation == drawing_data['building_name']:
                    drawing_file = drawing.file
                    file_url = str(drawing_file.file_field.path)
                    if os.path.isfile(file_url):
                        print(file_url)
                        os.remove(file_url)
                    drawing_file.file_field=files[0]
                    drawing_file.save(update_fields=['file_field'])
                    return HttpResponseRedirect('/success/')
                form.add_error('file_field', f'The file name"{files[0].name}" does not match the drawing being updated.')
                form.clean()
                return render(request, self.template_name, {'form': form})
            for error in list_of_errors:
                form.add_error('file_field', error)
            form.add_error('file_field', 'No file has been saved, please correct the above errors.')
            form.clean()
            return render(request, self.template_name, {'form': form})
        return render(request, self.template_name, {'form': form})
