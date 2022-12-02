import re
from .models import Project, BuildingName, DrawingFile


def drawings_name_checker(name):
    check=re.search(r'^[A-Z0-9]{1,3}_[A-Z0-9]{1,3}_[A-Z0-9]{1,3}_[A-Z0-9]{1,3}_[0-9.]{1,10}_[A-Z]{1,3}_[0-9]{4}-[0-9]{2}-[0-9]{2}_[a-zA-Z0-9- ]*[.]pdf', name)
    if check:
        name_list = name.split('_')
        if '.pdf' in name_list[7]:
            name_list[7] = name_list[7][:-4]
        drawing_data = {
            'project': name_list[0],
            'design_stage': name_list[1],
            'branch': name_list[2],
            'building_name': name_list[3],
            'draw_number': name_list[4],
            'revision': name_list[5],
            'date_drawing': name_list[6],
            'draw_title': name_list[7],
        }
        return drawing_data
    return {}


def files_checker(files,project_id):
    list_of_errors=[]
    for file in files:
        drawing_data = drawings_name_checker(file.name)
        if drawing_data:
            project = Project.objects.get(id=project_id)
            if project.abbreviation == drawing_data['project']:
                building_name = BuildingName.objects.filter(abbreviation=drawing_data['building_name']).first()
                if building_name:
                    file_name = "_".join(file.name.split("_")[0:6])
                    if not DrawingFile.objects.filter(file_name=file_name):
                        continue
                    list_of_errors.append(f'File "{file.name}" already exists')
                    continue
                list_of_errors.append(f'The building name in the file name "{file.name}" does not exist')
                continue
            list_of_errors.append(f'The project name in the file name "{file.name}" is invalid')
            continue
        list_of_errors.append( f'Please send the file "{file.name}" with the correct name')
        continue
    return list_of_errors


