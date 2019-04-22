import great_expectations as ge
import os

class FileValidator(object):

    def __init__(self, columns=None, expectations=None):
        self.expectations=expectations
        self.columns = columns
    
    def _get_file_extension(self, file_):
        filename, extension = os.path.splitext(file_)
        allowed_types = ['.csv','.gz']
        if extension not in allowed_types:
            raise RuntimeError("Supported files type: {0}".format(allowed_types))
        else:
            return extension
    
    def _open_file(self, file):
        if (os.path.isfile(file)):
            extension = self._get_file_extension(file)
            if extension.__eq__(".gz"):
                return ge.read_csv(filename=file, compression="gzip", names=self.columns)
            else:
                return ge.read_csv(filename=file, names=self.columns)
        else:
            raise RuntimeError("File {0} doesn't exist".format(file))

    def _run_expectations(self, data):
        results = data.validate(expectations_config=self.expectations, result_format='BOOLEAN_ONLY')
        del data
        return results
    
    def validate(self,file):
        results = self._run_expectations(self._open_file(file))
        results['file_path'] = file 
        return results