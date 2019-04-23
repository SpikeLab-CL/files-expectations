import os
import subprocess
import sys
import logging
import tempfile
import shutil

logging.basicConfig(level=logging.INFO)

class GoogleStorage(object):
    temp_folder = None

    def __init__(self, credential_path=None):
        #TODO 
        # Allow to use services accounts
        # For now only works with machines with gsutil 
        # properly configurated  
        self.credential_path = credential_path

    def file_exists_in_gcs(self, gs_file_path): #this works with wildcards too
        logging.info("Checking if file(s) exists in {0}".format(gs_file_path))
        cmd = "gsutil -q stat {0}".format(gs_file_path)
        proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True,
                            universal_newlines=True)
        proc.communicate()
        if(proc.returncode == 0):
            return True
        else:
            raise RuntimeError("File or folder {0} doesn't exist".format(gs_file_path))
    
    def download_files(self, gs_file_path):
        logging.info("Downloading file(s) from {0}".format(gs_file_path))
        try:
            self.temp_folder = tempfile.mkdtemp()
            logging.info("Storing files at {0}".format(self.temp_folder))
            subprocess.check_call(['gsutil','-q','cp', gs_file_path, self.temp_folder], stderr=sys.stdout)
        except Exception as e:
            raise RuntimeError("Error while downloading the input files")
    
    def clean_temp_folder(self):
        try:
            logging.info("Cleaning files from {0}".format(self.temp_folder))
            shutil.rmtree(self.temp_folder)
        except OSError as e:
            raise
    
    def move_storage_file(self, original_path, destination_path):
        logging.info("Moving file {0} to {1}".format(original_path, destination_path))
        try:
            subprocess.check_call(['gsutil','mv', original_path, destination_path], stderr=sys.stdout)
        except Exception as e:
            logging.warning("Error moving the file {0} to {1}".format(original_path, destination_path))