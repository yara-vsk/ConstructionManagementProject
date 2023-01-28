import os
import shutil

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.generic import CreateView, View, ListView, DeleteView, UpdateView

from ConstrManagementProject.settings import BASE_DIR, MEDIA_ROOT
from .custommixins import CustomPermMixin
from .form import BuildingNameForm, UploadDrawingForm, ProjectForm, DrawingsSearchForm, MembersOfProjectForm, \
    DrawingUserForm
from django.http import HttpResponseRedirect, Http404, FileResponse
from .models import DrawingFile, Drawing, BuildingName, Project, MemberOfProject, DrawingUser
from .drawingsnamechecker import drawings_name_checker
from .fileschecker import files_checker
from datetime import datetime, timezone


class ProjectListView(CustomPermMixin, View):
    template_name = 'drawingdoc/projects_list.html'
    permission_required = 'drawingdoc.view_project'

    def get(self, request, *args, **kwargs):
        user = request.user
        user_projects = MemberOfProject.objects.filter(user=user).all()
        return render(request, self.template_name, {'object_list': user_projects})


class ProjectInfoView(CustomPermMixin, View):
    template_name = 'drawingdoc/project_info.html'
    permission_required = 'drawingdoc.view_project'

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs['pk_p'])
        building_names = BuildingName.objects.filter(project=project.id).all()
        return render(request, self.template_name, {'project': project, 'building_list': building_names})


class NewBuildingName(CustomPermMixin, View):
    form_class = BuildingNameForm
    template_name = 'drawingdoc/newbuildingname.html'
    permission_required = 'drawingdoc.add_buildingname'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        try:
            project = Project.objects.get(id=kwargs['pk_p'])
        except Project.DoesNotExist:
            raise Http404("Project does not exist")
        form = self.form_class(request.POST)
        if form.is_valid():
            building_name = BuildingName(
                name=form.cleaned_data['name'],
                abbreviation=form.cleaned_data['abbreviation'].upper(),
                project=project,
            )
            building_name.save()
            return HttpResponseRedirect(reverse_lazy('project:project-info', kwargs={"pk_p": kwargs["pk_p"]}))
        return render(request, self.template_name, {'form': form})


class BuildingNameDeleteView(CustomPermMixin, View):
    permission_required = 'drawingdoc.delete_buildingname'

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs['pk_p'])
        building_name = get_object_or_404(BuildingName, pk=kwargs['pk_bn'])
        drawing_list = Drawing.objects.filter(building_name=building_name, project=project)
        for drawing in drawing_list:
            file_url = str(drawing.file.file_field.path)
            if os.path.isfile(file_url):
                os.remove(file_url)
            drawing.file.delete()
        building_name.delete()
        return HttpResponseRedirect(reverse_lazy('project:project-info', kwargs={"pk_p": self.kwargs["pk_p"]}))


class BuildingNameUpdateView(CustomPermMixin, UpdateView):
    form_class = BuildingNameForm
    model = BuildingName
    pk_url_kwarg = "pk_bn"
    template_name = 'drawingdoc/newbuildingname.html'
    permission_required = 'drawingdoc.change_buildingname'

    def get_success_url(self):
        return reverse_lazy('project:project-info', kwargs={"pk_p": self.kwargs["pk_p"]})


class NewProjectView(CustomPermMixin, View):
    form_class = ProjectForm
    template_name = 'drawingdoc/newbuildingname.html'
    permission_required = 'drawingdoc.add_project'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            project = Project(
                name=form.cleaned_data['name'],
                abbreviation=form.cleaned_data['abbreviation'].upper(),
                creator=get_user_model().objects.get(id=request.user.id),
            )
            project.save()
            content_type = ContentType.objects.get_for_model(Project)
            permission = Permission.objects.create(
                codename='project_'+str(project.id),
                name='Can use project with id='+str(project.id),
                content_type=content_type,
            )
            permission.save()
            user=request.user
            user.user_permissions.add(permission)
            user.save()
            member_of_project = MemberOfProject(
                user=user,
                project=project
            )
            member_of_project.save()
            return HttpResponseRedirect(reverse_lazy('project:project-list'))
        return render(request, self.template_name, {'form': form})


class AddUserToProjectView(CustomPermMixin, View):
    form_class = MembersOfProjectForm
    template_name = 'drawingdoc/newbuildingname.html'
    permission_required = 'drawingdoc.add_memberofproject'

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs['pk_p'])
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs['pk_p'])
        form = self.form_class(request.POST)
        if form.is_valid():
            user = get_user_model().objects.get(email=form.cleaned_data['email'])
            if MemberOfProject.objects.filter(user=user,project=project):
                form.add_error('email', 'The user is already a member of the project')
                form.clean()
                return render(request, self.template_name, {'form': form})
            member_of_project = MemberOfProject(
                user=user,
                status_user_perms = form.cleaned_data['status_user_perms'],
                project=project,
            )
            member_of_project.save()
            permission = Permission.objects.get(
                codename='project_'+str(project.id),
                content_type=ContentType.objects.get_for_model(Project),
            )
            user.user_permissions.add(permission)
            user.save()
            return HttpResponseRedirect(reverse_lazy('project:members',kwargs={"pk_p": self.kwargs["pk_p"]}))
        return render(request, self.template_name, {'form': form})


class MemberOfProjectListView(CustomPermMixin, View):
    template_name = 'drawingdoc/members_of_project_list.html'
    permission_required = 'drawingdoc.add_memberofproject'

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs['pk_p'])
        members_of_project = MemberOfProject.objects.filter(project=project)
        return render(request, self.template_name, context={'members_of_project':members_of_project, 'project':project})


class MemberOfProjectDeleteView(CustomPermMixin, View):

    permission_required = 'drawingdoc.delete_memberofproject'

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs['pk_p'])
        members_of_project = get_object_or_404(MemberOfProject, pk=kwargs['pk_m'])
        user = request.user
        permission = Permission.objects.get(
            codename='project_' + str(project.id),
            content_type=ContentType.objects.get_for_model(Project),
        )
        members_of_project.delete()
        user.user_permissions.remove(permission)
        user.save()
        return HttpResponseRedirect(reverse_lazy('project:members', kwargs={"pk_p": kwargs["pk_p"]}))


class UploadDrawingView(CustomPermMixin, View):
    form_class = UploadDrawingForm
    template_name = 'drawingdoc/uploaddrawing.html'
    permission_required = 'drawingdoc.add_drawing'

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

                    activity = DrawingUser(
                        drawing = drawing,
                        user = request.user,
                        date = datetime.now(timezone.utc),
                        status = DrawingUser.Status.s3,
                    )
                    activity.save()
                return HttpResponseRedirect(reverse_lazy('project:project-info', kwargs={"pk_p": kwargs["pk_p"]}))
            for error in list_of_errors:
                form.add_error('file_field', error)
            form.add_error('file_field', 'No file has been saved, please correct the above errors')
            form.clean()
            return render(request, self.template_name, {'form': form})
        return render(request, self.template_name, {'form': form})


class DrawingsListView(CustomPermMixin, View):
    template_name = 'drawingdoc/drawings_list.html'
    permission_required = 'drawingdoc.view_drawing'

    def get(self, request, *args, **kwargs):
        revision_list = []
        object_dict = {}
        drawing_number_list = []
        try:
            project = Project.objects.get(id=kwargs['pk_p'])
        except Project.DoesNotExist:
            raise Http404("Project does not exist")
        form = DrawingsSearchForm(request.GET, project.id)
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
                                                                         'draw_number', 'draw_title',
                                                                         'building_name__abbreviation',
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


class DrawingInfoView(CustomPermMixin, View):
    template_name = 'drawingdoc/drawing_info.html'
    permission_required = 'drawingdoc.view_drawing'
    form_class = DrawingUserForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        project = get_object_or_404(Project, pk=kwargs['pk_p'])
        drawing = get_object_or_404(Drawing, pk=kwargs['pk'])
        activities = DrawingUser.objects.filter(drawing=drawing).order_by('date').all()
        drawing_status = DrawingUser.objects.filter(drawing=drawing).order_by('-date').first()
        return render(request, self.template_name, {'obj': drawing,
                                                    'activities':activities,
                                                    'dr_status':drawing_status,
                                                    'form':form
                                                    })

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs['pk_p'])
        drawing = get_object_or_404(Drawing, pk=kwargs['pk'])
        form = self.form_class(request.POST)
        if form.is_valid():
            activity = DrawingUser(
                drawing=drawing,
                user=request.user,
                date=datetime.now(timezone.utc),
                comment=form.cleaned_data['comment'],
                status=form.cleaned_data['status']
            )
            activity.save()
        return HttpResponseRedirect(reverse_lazy('project:drawing-document-info', kwargs={"pk_p": kwargs["pk_p"],
                                                                                          "pk": kwargs["pk"]}))


class DrawingDeleteView(CustomPermMixin, View):
    permission_required = 'drawingdoc.delete_drawing'

    def get(self, request, *args, **kwargs):
        try:
            drawing = Drawing.objects.get(id=kwargs['pk'])
            file_url = str(drawing.file.file_field.path)
            drawing.file.delete()
            if os.path.isfile(file_url):
                os.remove(file_url)
        except Drawing.DoesNotExist:
            raise Http404("Drawing does not exist")
        return HttpResponseRedirect(reverse_lazy('project:drawing-document-list', kwargs={"pk_p": kwargs["pk_p"]}))



class DrawingUpdateView(CustomPermMixin, View):
    form_class = UploadDrawingForm
    template_name = 'drawingdoc/uploaddrawing.html'
    permission_required = ('drawingdoc.change_drawing', 'drawingdoc.add_drawingfile',
                           'drawingdoc.change_drawingfile', 'drawingdoc.delete_drawingfile')

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
                        os.remove(file_url)
                    drawing_file.file_field = files[0]
                    drawing_file.save(update_fields=['file_field'])

                    activity = DrawingUser(
                        drawing=drawing,
                        user=request.user,
                        date=datetime.now(timezone.utc),
                        status=DrawingUser.Status.s3
                    )
                    activity.save()
                    return HttpResponseRedirect(reverse_lazy('project:drawing-document-info',
                                                             kwargs={"pk_p": kwargs["pk_p"], "pk": drawing.id}))
                form.add_error('file_field',
                               f'The file name"{files[0].name}" does not match the drawing being updated.')
                form.clean()
                return render(request, self.template_name, {'form': form})
            for error in list_of_errors:
                form.add_error('file_field', error)
            form.add_error('file_field', 'No file has been saved, please correct the above errors.')
            form.clean()
            return render(request, self.template_name, {'form': form})
        return render(request, self.template_name, {'form': form})


class HomeView(ListView):
    template_name = 'drawingdoc/home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class ProjectDeleteView(CustomPermMixin, DeleteView):
    template_name = 'drawingdoc/generic_delete.html'
    model = Project
    pk_url_kwarg = "pk_p"
    permission_required = 'drawingdoc.delete_project'

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs['pk_p'])
        file_url = os.path.join(BASE_DIR, 'media/uploads/' + str(project.abbreviation))

        drawing_list = Drawing.objects.filter(project=project)
        for drawing in drawing_list:
            drawing.file.delete()

        if os.path.isdir(file_url):
            shutil.rmtree(file_url)
        project.delete()
        return HttpResponseRedirect(reverse_lazy('project:project-list'))


@xframe_options_sameorigin
@permission_required('drawingdoc.view_drawingfile', login_url='/login/')
def media_access(request, path):
    response = FileResponse(open(MEDIA_ROOT+'/'+path[:], 'rb'))
    return response
