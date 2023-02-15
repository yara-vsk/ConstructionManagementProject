from django.urls import path, reverse_lazy, include
from django.views.generic import RedirectView

from .views import UploadCsvView, ScheduleView

urlpatterns = [
    path('upload/', UploadCsvView.as_view(),name='schedule-upload'),
    path('', ScheduleView.as_view(),name='schedule-view'),
]