### Spike Great Expectations validator

Validate multiples `.csv` files using [Great Expectations](https://github.com/great-expectations/great_expectations) framework.

#### Instalation:
Install the requirements using:
`
pip install -r requirements.txt
`

#### Usage:
You can validate your files using:
```
python main.py
  --validation_file VALIDATION_FILE
                        Great expectations .json file
  --input_files INPUT_FILES
                        Path to .csv files, could be local files or GCS files
  --columns COLUMNS     OPTIONAL .csv file columns names
  --successful_dest_folder SUCCESSFUL_DEST_FOLDER
                        OPTIONAL Folder to move sucessful validations files
  --failed_dest_folder FAILED_DEST_FOLDER
                        OPTIONAL Folder to move failed validations files
```

Where:

`--validation_file`: is the `great_expectation output` json file. <br>
`--input_files`: could be a single file, or multiples files using a wildcard in the name (`/my_file.csv` or `/my_files_*.csv`). You can provide a local file path `/home/user/data/files_*.csv` or a Google Cloud Storage path `gs://bucket/data/files_*.csv`. <br>
`--columns`: **OPTIONAL** You can provide the `.csv` header `"['var1','var2',...'varN']"` <br>
`--successful_dest_folder`: **OPTIONAL** Move the successful validated files into this folder (`path/to/my_folder/` or `gs://path/to/my_folder/`) <br>
`--failed_dest_folder`: **OPTIONAL** Move the failed validated files into this folder (`path/to/my_folder/` or `gs://path/to/my_folder/`) <br>

The **output** are two files:

`failed_results_dd-MM-YYY-hh:ss:mm.json`: Which contains the failed `expectations` <br>
`successful_results_dd-MM-YYY-hh:ss:mm.json`: Summary with the successfull `expectations`