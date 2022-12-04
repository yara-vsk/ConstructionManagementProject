from django.urls import path, reverse_lazy
from .views import NewDrawing, NewBuildingName, UploadDrawingView, NewProjectView, DrawingsListView, DrawingInfoView, DrawingDeleteView

from .models import Drawing


urlpatterns = [
    path('new/', NewDrawing.as_view()),
    path('new_building_name/', NewBuildingName.as_view()),
    path('new_project/', NewProjectView.as_view()),
    path('upload/', UploadDrawingView.as_view()),
    path('list/', DrawingsListView.as_view(),name='drawings-list'),
    path('<int:pk>/', DrawingInfoView.as_view()),
    path('<int:pk>/delete/', DrawingDeleteView.as_view()),
]