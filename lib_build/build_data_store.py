import datetime
import os

class BuildDataStore:
    def __init__(self, dir_name):
        self.dir_name = dir_name

    def create_data_store_folder(self):
        try:
            base_dir = os.getcwd()
            data_store_dir = os.path.join(base_dir, self.dir_name)
            
            if not os.path.exists(data_store_dir):
                os.makedirs(data_store_dir)
                with open('log\log_build.txt', 'a+') as file:
                    file.write(
                        f"{datetime.datetime.now()} SUCCESS Created {self.dir_name} folder at {data_store_dir} \n")
            
            subfolders = ['cpa', 'process', 'pre_data', 'post_data', 'exp']
            for subfolder in subfolders:
                folder_path = os.path.join(data_store_dir, subfolder)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                    with open('log\log_build.txt', 'a+') as file:
                        file.write(
                            f"{datetime.datetime.now()} SUCCESS Created '{subfolder}' folder at {folder_path} \n")
        except Exception as e:
            with open('log\log_build.txt', 'a+') as file:
                file.write(
                    f"{datetime.datetime.now()} ERROR ON CREATE DATA STORE FOLDER {self.dir_name}: {e} \n")

    def clear_subfolders(self):
        try:
            base_dir = os.getcwd()
            data_store_dir = os.path.join(base_dir, self.dir_name)

            subfolders = ['cpa', 'process', 'pre_data', 'post_data', 'exp']
            for subfolder in subfolders:
                folder_path = os.path.join(data_store_dir, subfolder)
                if os.path.exists(folder_path):
                    for file_name in os.listdir(folder_path):
                        file_path = os.path.join(folder_path, file_name)
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                    with open('log\log_build.txt', 'a+') as file:
                        file.write(
                            f"{datetime.datetime.now()} SUCCESS Cleared '{subfolder}' folder at {folder_path} \n")

        except Exception as e:
            with open('log\log_build.txt', 'a+') as file:
                file.write(
                    f"{datetime.datetime.now()} ERROR ON CLEAR DATA STORE FOLDER {self.dir_name}: {e} \n")
