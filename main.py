import argparse
from utils import open_expectations, parse_results, write_results, pre_process_args
from files_validator import FileValidator
from files_handler import FilesHandler
from multiprocessing import Pool, cpu_count, Manager
from tqdm import tqdm
import logging
import ast

logging.basicConfig(level=logging.INFO)

def main(args):
    expectations, input_files, columns = pre_process_args(args)
    files = FilesHandler(input_files=input_files)
    files_path = files.get_files_path()
    
    validator = FileValidator(columns=columns, expectations=expectations)
    
    logging.info(" Starting the validation files process.. ")
    p = Pool(processes=cpu_count())
    r = list(tqdm(p.imap(validator.validate, files_path), total=len(files_path)))
    p.close()
    p.join()

    sucessful,failed = parse_results(r)
    write_results(sucessful, success=True)
    write_results(failed, success=False)

    if(files.is_from_storage):
        files.clean_temp_folder()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='spike .csv validator')
    parser.add_argument('--validation_file', type=str, required=True, help='Great expectations .json file')
    parser.add_argument('--input_files', type=str, required=True, help='Path to .csv files, could be local files or GCS files')
    parser.add_argument('--columns', default=None, required=False, help="OPTIONAL .csv file columns names")
    args = parser.parse_args()
    main(args)