import os
import json
import logging
logging.basicConfig(level=logging.INFO)
from datetime import datetime
import os
import ast

def pre_process_args(args):
    expectations = open_expectations(args.validation_file)
    input_files = args.input_files
    columns = ast.literal_eval(args.columns) if args.columns is not None else None
    return expectations, input_files, columns

def open_expectations(file_path):
    logging.info(" Trying to load expectations from {0}".format(file_path))
    try:
        if(os.path.isfile(file_path)):
            with open(file_path) as file:
                return json.load(file)
        else:
            raise RuntimeError("File {0} doesn't exist".format(file_path))
    except Exception as e:
        raise RuntimeError("Can't open {0}".format(file_path))

def parse_results(expectations):
    success = []
    failed = []
    for expectation in expectations:
        try:
            d = {}
            d['statistics'] = expectation['statistics']
            d['file_path'] = expectation['file_path']
            success_percent = expectation['statistics']['success_percent']
            if success_percent == 100.0:
                success.append(d)
            else:
                d['results'] = list(filter(lambda x: x['success'] == False, expectation['results']))
                failed.append(d)
        except Exception as e:
            logging.warning("Error reading expectations from file {0}".format(expectation['file_path']))
    return success, failed

def write_results(expectations, success=True):
    now = datetime.now().strftime("%m-%d-%Y-%H:%M:%S")
    r = {}
    r['expectations'] = expectations
    if success:
        file_name = "{0}/successful_results_{1}.json".format(os.getcwd(), now)
        logging.info(" Writing full successfull expectations in {0}".format(file_name))
    else:
        file_name = "{0}/failed_results_{1}.json".format(os.getcwd(), now)
        logging.info(" Writing failed expectations in {0}".format(file_name))
    f = open(file_name, "w+")
    f.write(json.dumps(r, indent=4,))
    f.close()

        
