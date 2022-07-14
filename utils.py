import json 

def reset_json(file_name):
    with open('snapshot/'+file_name, 'w') as f:
        json.dump([], f, indent=4)