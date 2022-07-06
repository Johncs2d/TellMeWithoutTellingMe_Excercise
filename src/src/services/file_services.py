import csv
import json


class FileHandlerService:
    def __init__(self, type, *args, **kwargs):
        self.__type = type

    def __csv_reader(self, file):
        try:
            rows = []
            reader =  csv.DictReader(file)
            for item in reader:
                rows.append(item)

            return rows
        except csv.Error:
            raise ValueError("File content is not a valid CSV")

    def __json_reader(self, file):
        try:
            return json.load(file)
        except ValueError:
            raise ValueError("Invalid JSON File")

    def read(self, file):
        if self.__type == 'json':
            return self.__json_reader(file)

        return self.__csv_reader(file)

class FileReaderService:
    def __init__(self, file_handler: FileHandlerService, duplicates=False):
        self.__file_handler = file_handler
        self.__duplicates = duplicates

    def to_model_objects(self, file, model, **kwargs):
        file_data = self.__file_handler.read(file)
        if self.__duplicates == False:
            file_data = self._clean(file_data)

        instances = []

        for item in file_data:
            instances.append(model(**item, **kwargs))

        return instances, file_data

    def _clean(self, file_data):
        return list({frozenset(item.items()):item for item in file_data}.values())
