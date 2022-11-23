from django.urls import path
from .views import NewDrawing, NewBuildingName, upload_drawing


urlpatterns = [
    path('new/', NewDrawing.as_view()),
    path('new_building_name/', NewBuildingName.as_view()),
    path('upload/', upload_drawing),
]