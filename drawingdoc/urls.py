from django.urls import path
from .views import NewDrawing, NewBuildingName, UploadDrawingView, NewProjectView


urlpatterns = [
    path('new/', NewDrawing.as_view()),
    path('new_building_name/', NewBuildingName.as_view()),
    path('new_project/', NewProjectView.as_view()),
    path('upload/', UploadDrawingView.as_view()),
]