from django.shortcuts import render
from django.views.generic import CreateView, ListView
from .form import BuildingNameForm, DrawingForm
# Create your views here.


class NewDrawing(CreateView):
    form_class = DrawingForm
    template_name = 'drawingdoc/newbuildingname.html'
    success_url = '/'


class NewBuildingName(CreateView):
    form_class = BuildingNameForm
    template_name = 'drawingdoc/newbuildingname.html'
    success_url = '/'


def upload_drawing(request):
    if request.method == "POST":
        uploaded_file = request.FILES['drawing']
        print(uploaded_file.name)
    return render(request, 'drawingdoc/uploaddrawing.html')