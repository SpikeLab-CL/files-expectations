import os
import glob
from storage import GoogleStorage
import logging
import subprocess
import sys

logging.basicConfig(level=logging.INFO)

class FilesHandler(GoogleStorage):
    def __init__(self, input_files, credential_path=None):
        super(FilesHandler, self).__init__()
        self.input_files = input_files
        if(self.is_from_storage):
            pass
            if(self.file_exists_in_gcs(self.input_files)):
                self.download_files(self.input_files)
        else:
            logging.info("Reading file(s) from {0}".format(input_files))
    
    @property
    def is_from_storage(self):
        return self.input_files.startswith("gs://")

    @property
    def file_name(self):
        return self.input_files.split("/")[-1]
    
    def get_original_folder(self):
        return "/".join(self.input_files.split("/")[0:-1])+"/"

    def get_files_path(self):
        if(self.is_from_storage):
            files_path = glob.glob("{path}/{file}".format(path=self.temp_folder,
                                                          file=self.file_name))
            return files_path
        else:
            files_path = glob.glob(self.input_files)
            if len(files_path) == 0:
                raise RuntimeError("Error, no file(s) at {0}".format(self.input_files))
            else:
                return files_path
    
    def move_file(self, file_name, destination_path):
        original_path = self.get_original_folder()
        if(self.is_from_storage):
            self.move_storage_file(original_path+file_name,destination_path+file_name)
        else: 
            try:
                subprocess.check_call(['mv', original_path+file_name,
                                             destination_path+file_name], stderr=sys.stdout)
            except Exception as e:
                logging.warning("Error moving file from s{0} to {1}".format(original_path+file_name, 
                                                                          destination_path+file_name))

if __name__ == "__main__":
    path = "gs://spike-kwik-pruebas/trx/trx_*.csv.gz"
    f = FilesHandler(input_files=path)
