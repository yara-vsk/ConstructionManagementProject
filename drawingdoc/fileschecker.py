import re
from .models import Project, BuildingName, DrawingFile, Drawing
from .drawingsnamechecker import drawings_name_checker

def files_checker(files,project_id):
    list_of_errors=[]
    for file in files:
        drawing_data = drawings_name_checker(file.name)
        if drawing_data:
            project = Project.objects.get(id=project_id)
            building_name = BuildingName.objects.filter(abbreviation=drawing_data['building_name']).first()
            file_name = "_".join(file.name.split("_")[0:6])
            if not project.abbreviation == drawing_data['project']:
                list_of_errors.append(f'The project name in the file name "{file.name}" is invalid')
            if not building_name:
                list_of_errors.append(f'The building name in the file name "{file.name}" does not exist')
            if DrawingFile.objects.filter(file_name=file_name):
                list_of_errors.append(f'File "{file.name}" already exists')
            if drawing_data['design_stage'] not in Drawing.DesignStage:
                list_of_errors.append(f'The design stage specified in the file "{file.name}" does not exist')
            if drawing_data['branch'] not in Drawing.Branch:
                list_of_errors.append(f'The branch specified in the file "{file.name}" does not exist')
            continue
        list_of_errors.append( f'Please send the file "{file.name}" with the correct name')
        continue
    return list_of_errors
