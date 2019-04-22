import os
import glob
from storage import GoogleStorage
import logging
logging.basicConfig(level=logging.INFO)

class FilesHandler(GoogleStorage):
    def __init__(self, input_files, credential_path=None):
        super(FilesHandler, self).__init__()
        self.input_files = input_files
        if(self.is_from_storage):
            if(self.file_exists_in_gcs(self.input_files)):
                self.download_files(self.input_files)
        else:
            logging.info(" Reading file(s) from {0}".format(input_files))
    
    @property
    def is_from_storage(self):
        return self.input_files.startswith("gs://")

    @property
    def file_name(self):
        return self.input_files.split("/")[-1]
    
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
