import datetime
import json
import os


def data_receiver(save_path:str, contents):
    try: 
        if 'data_store/cpa' in save_path:
            if len(save_path.split('/')) != 5:
                with open('log/log_upload.txt', 'a+') as file:
                    file.write(f"{datetime.datetime.now()} ERROR ON UPLOADING: {save_path}: path error \n")
                return 'path error'
            else:
                if not os.path.exists(save_path.rsplit('/', 1)[0]):
                    os.makedirs(save_path.rsplit('/', 1)[0])
        
        with open(save_path, "wb") as f:
            f.write(contents)

        with open('log/log_upload.txt', 'a+') as file:
            file.write(
                f"{datetime.datetime.now()} SUCCESS ON UPLOADING: {save_path} \n")
        return 'success'
    
    except Exception as e:
        with open('log/log_upload.txt', 'a+') as file:
            file.write(
                f"{datetime.datetime.now()} ERROR ON UPLOADING: {save_path}: {e} \n")
        return 'error'
    
def dict_to_txt(dict_form_str_data):
    dict_data = json.loads(dict_form_str_data)
    content = ''
    for key, value in dict_data.items():
        content+=(f'{key}: {value}\n')
    
    return content.encode('utf-8')