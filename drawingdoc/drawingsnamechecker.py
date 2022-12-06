import re



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



