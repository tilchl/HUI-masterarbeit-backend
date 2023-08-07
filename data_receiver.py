import datetime
import json
import os
import ast

def data_receiver(save_path, contents, data_type):
    try: 
        if data_type == 'CPA':
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
    
def dict_to_txt(dict_form_str_data, data_type, file_name):
    try:
        dict_data = json.loads(dict_form_str_data)
        if data_type == 'Experiment':
        #     content = '{'
        #     for key, value in dict_data.items():
        #         content+=(f'"{key}": {value},')
        #     content = content[:-1] + "}"
            return str(dict_data).replace("'", '"').encode('utf-8')
        elif data_type == 'CPA':
            cpa_type = file_name.split('/')[1]
            if cpa_type == 'DSC':
                content = ''
                curve_content = ''
                for key, value in dict_data.items():
                    if key == 'Curve':
                        curve_content = '\n##' + value
                    else:
                        content+=(f'#{key}: {value}\n')
                content+= curve_content
            elif cpa_type == 'FTIR':
                content = '#DATA\n'
                curve_content = ''
                for key, value in dict_data.items():
                    if key == 'Curve':
                        curve_content = '\n##' + value.replace(';', '\t')
                    else:
                        content+=(f'{key}: {value}\n')
                content+= curve_content
            else:
                content = ''
                curve_content = ''
                for key, value in dict_data.items():
                    if key == 'Curve':
                        curve_content = '\n##' + value
                    else:
                        content+=(f'{key}: {value}\n')
                content+= curve_content
            return content.encode('utf-8')

        else:
            content = ''
            for key, value in dict_data.items():
                content+=(f'{key}: {value}\n')
            return content.encode('utf-8')
    
    except Exception as e:
        with open('log/log_upload.txt', 'a+') as file:
            file.write(
                f"{datetime.datetime.now()} ERROR ON UPLOADING: {file_name}: {e} \n")
        return 'error'