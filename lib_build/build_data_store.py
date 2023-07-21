import datetime
import os
import shutil


class BuildDataStore:
    def __init__(self, dir_name):
        self.dir_name = dir_name

    def create_data_store_folder(self):
        try:
            base_dir = os.getcwd()
            data_store_dir = os.path.join(base_dir, self.dir_name)

            if not os.path.exists(data_store_dir):
                os.makedirs(data_store_dir)
                with open('log/log_build.txt', 'a+') as file:
                    file.write(
                        f"{datetime.datetime.now()} SUCCESS Created {self.dir_name} folder at {data_store_dir} \n")

                subfolders = ['CPA', 'Process', 'PreData', 'PostData', 'Experiment']
                for subfolder in subfolders:
                    folder_path = os.path.join(data_store_dir, subfolder)
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)
                        with open('log/log_build.txt', 'a+') as file:
                            file.write(
                                f"{datetime.datetime.now()} SUCCESS Created '{subfolder}' folder at {folder_path} \n")
                return 'success'
            else:
                with open('log/log_build.txt', 'a+') as file:
                    file.write(
                        f"{datetime.datetime.now()} ERROR Created {self.dir_name} folder at {data_store_dir}: already exists \n")
                return 'exists'
        except Exception as e:
            with open('log/log_build.txt', 'a+') as file:
                file.write(
                    f"{datetime.datetime.now()} ERROR ON CREATE DATA STORE FOLDER {self.dir_name}: {e} \n")
            return 'error'

    def delete_folder(self):
        try:
            base_dir = os.getcwd()
            data_store_dir = os.path.join(base_dir, self.dir_name)
            shutil.rmtree(data_store_dir)
            with open('log/log_build.txt', 'a+') as file:
                        file.write(
                            f"{datetime.datetime.now()} SUCCESS Deleted folder: {data_store_dir} \n")
            return 'success'
        except Exception as e:
            with open('log/log_build.txt', 'a+') as file:
                file.write(
                    f"{datetime.datetime.now()} ERROR ON DELETE DATA STORE FOLDER {self.dir_name}: {e} \n")
            return 'error'
    
    def delete_one_type(self, data_type):
        try:
            base_dir = os.getcwd()
            data_store_dir = os.path.join(base_dir, f'{self.dir_name}/{data_type}')
            shutil.rmtree(data_store_dir)
            with open('log/log_build.txt', 'a+') as file:
                        file.write(
                            f"{datetime.datetime.now()} SUCCESS Deleted folder: {data_store_dir} \n")
            return 'success'
        except Exception as e:
            with open('log/log_build.txt', 'a+') as file:
                file.write(
                    f"{datetime.datetime.now()} ERROR ON DELETE DATA STORE FOLDER {data_store_dir}: {e} \n")
            return 'error'
        
    def create_one_type(self, data_type):
        try:
            base_dir = os.getcwd()
            data_store_dir = os.path.join(base_dir, f'{self.dir_name}/{data_type}')
            if not os.path.exists(data_store_dir):
                os.makedirs(data_store_dir)
                with open('log/log_build.txt', 'a+') as file:
                            file.write(
                                f"{datetime.datetime.now()} SUCCESS Created folder: {data_store_dir} \n")
                return 'success'
            else:
                with open('log/log_build.txt', 'a+') as file:
                            file.write(
                                f"{datetime.datetime.now()} ERROR Created folder: {data_store_dir}: already exists \n")
                return 'exists'
        except Exception as e:
            with open('log/log_build.txt', 'a+') as file:
                file.write(
                    f"{datetime.datetime.now()} ERROR Created folder {self.dir_name}: {e} \n")
            return 'error'