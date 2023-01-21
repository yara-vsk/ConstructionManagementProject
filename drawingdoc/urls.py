from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from .views import NewBuildingName, UploadDrawingView, NewProjectView, DrawingsListView, DrawingInfoView, \
    DrawingDeleteView, DrawingUpdateView, ProjectListView, ProjectInfoView, BuildingNameDeleteView,\
    BuildingNameUpdateView, ProjectDeleteView, AddUserToProjectView, MemberOfProjectListView, MemberOfProjectDeleteView



urlpatterns = [
    path('', RedirectView.as_view(url='list/')),
    path('new/', NewProjectView.as_view(), name='project-new'),
    path('list/', ProjectListView.as_view(), name='project-list'),
    path('<int:pk_p>/', ProjectInfoView.as_view(), name='project-info'),
    path('<int:pk_p>/delete/', ProjectDeleteView.as_view(), name='project-delete'),
    path('<int:pk_p>/members/', MemberOfProjectListView.as_view(), name='members'),
    path('<int:pk_p>/members/add/', AddUserToProjectView.as_view(), name='members-add'),
    path('<int:pk_p>/members/<int:pk_m>/delete/', MemberOfProjectDeleteView.as_view(), name='members-delete'),
    path('<int:pk_p>/building_name/<int:pk_bn>/delete/', BuildingNameDeleteView.as_view(),name='building-name-delete'),
    path('<int:pk_p>/building_name/<int:pk_bn>/update/', BuildingNameUpdateView.as_view(),name='building-name-update'),
    path('<int:pk_p>/new_building_name/', NewBuildingName.as_view(), name='building-name-create'),
    path('<int:pk_p>/drawing_documents/upload/', UploadDrawingView.as_view(),name='drawing-document-upload'),
    path('<int:pk_p>/drawing_documents/list/', DrawingsListView.as_view(),name='drawing-document-list'),
    path('<int:pk_p>/drawing_documents/<int:pk>/', DrawingInfoView.as_view(),name='drawing-document-info'),
    path('<int:pk_p>/drawing_documents/<int:pk>/delete/', DrawingDeleteView.as_view()),
    path('<int:pk_p>/drawing_documents/<int:pk>/update/', DrawingUpdateView.as_view()),
]