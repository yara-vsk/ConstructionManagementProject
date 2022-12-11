from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from .views import NewBuildingName, UploadDrawingView, NewProjectView, DrawingsListView, DrawingInfoView, \
    DrawingDeleteView, DrawingUpdateView, ProjectListView, ProjectInfoView

from .models import Drawing


urlpatterns = [
    path('', RedirectView.as_view(url='list/')),
    path('new/', NewProjectView.as_view()),
    path('list/', ProjectListView.as_view()),
    path('<int:pk_p>/', ProjectInfoView.as_view()),
    path('<int:pk_p>/new_building_name/', NewBuildingName.as_view()),
    path('<int:pk_p>/drawing_documents/upload/', UploadDrawingView.as_view()),
    path('<int:pk_p>/drawing_documents/list/', DrawingsListView.as_view()),
    path('<int:pk_p>/drawing_documents/<int:pk>/', DrawingInfoView.as_view()),
    path('<int:pk_p>/drawing_documents/<int:pk>/delete/', DrawingDeleteView.as_view()),
    path('<int:pk_p>/drawing_documents/<int:pk>/update/', DrawingUpdateView.as_view()),
]