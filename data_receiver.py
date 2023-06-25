import datetime
import os


def data_receiver(save_path:str, contents):
    try: 
        if 'data_store/cpa' in save_path:
            if not os.path.exists(save_path.rsplit('/', 1)[0]):
                os.makedirs(save_path.rsplit('/', 1)[0])
        
        with open(save_path, "wb") as f:
            f.write(contents)

        with open('log/log_upload.txt', 'a+') as file:
            file.write(
                f"{datetime.datetime.now()} SUCCESS ON UPLOADING: {os.path.basename(save_path)} \n")
        return 'success'
    
    except Exception as e:
        with open('log/log_upload.txt', 'a+') as file:
            file.write(
                f"{datetime.datetime.now()} ERROR ON UPLOADING: {os.path.basename(save_path)}: {e} \n")
        return 'error'