from django.urls import path, reverse_lazy, include
from django.views.generic import RedirectView

from .views import UploadCsvView, ScheduleGantView, ScheduleInfoView, ScheduleDeleteView

urlpatterns = [
    path('', ScheduleInfoView.as_view(), name='schedule-info'),
    path('upload/', UploadCsvView.as_view(), name='schedule-upload'),
    path('delete/', ScheduleDeleteView.as_view(), name='schedule-delete'),
    path('view/', ScheduleGantView.as_view(), name='schedule-view'),
]