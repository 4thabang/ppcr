from typing import List, Protocol


class Reader(Protocol):
    def read(self, file_path) -> List:
        """
        Read the contents of a file.

        Args:
            file_path(str): the file path where our csv will reside.

        Return:
            dict: the contents of a read document.
        """
        ...


class Writer(Protocol):
    def write(self, file_path, review):
        """
        Write the outputs of the review segmentation process to a file.

        Args:
            data(dict): the data that will populate the csv file.

        Return:
            bool: file write success status
        """
        ...


class ReadWriter(Protocol):
    def read(self, file_path) -> List:
        """
        Read the contents of a file.

        Args:
            file_path(str): the file path where our csv will reside.

        Return:
            dict: the contents of a read document.
        """
        ...

    def write(self, file_path, csv_content):
        """
        Write the outputs of the review segmentation process to a file.

        Args:
            data(dict): the data that will populate the csv file.

        Return:
            bool: file write success status
        """
        ...
