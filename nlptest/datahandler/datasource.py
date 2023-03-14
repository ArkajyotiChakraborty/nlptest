import os
import re
from abc import ABC, abstractmethod
from typing import List

import pandas as pd

from ..utils.custom_types import NEROutput, NERPrediction, Sample


class _IDataset(ABC):
    """Abstract base class for Dataset.

    Defines the load_data method that all subclasses must implement.
    """

    @abstractmethod
    def load_data(self):
        """Load data from the file_path."""
        return NotImplemented
    
    @abstractmethod
    def export_data(self):
        return NotImplemented


class DataFactory:
    """Data factory for creating Dataset objects.

    The DataFactory class is responsible for creating instances of the
    correct Dataset type based on the file extension.
    """

    def __init__(
            self,
            file_path: str
    ) -> None:
        """Initializes DataFactory object.

        Args:
            file_path (str): Path to the dataset.
        """

        self._file_path = file_path
        self._class_map = {cls.__name__.replace('Dataset', '').lower(): cls for cls in _IDataset.__subclasses__()}
        _, self.file_ext = os.path.splitext(self._file_path)

    def load(self):
        """Loads the data for the correct Dataset type.

        Returns:
            list[str]: Loaded text data.
        """
        self.init_cls = self._class_map[self.file_ext.replace('.', '')](self._file_path)
        return self.init_cls.load_data()

    def export(self, data: List[Sample], output_path:str):
        return self.init_cls.export_data(data, output_path)


class ConllDataset(_IDataset):
    """Class to handle Conll files. Subclass of _IDataset.
    """

    def __init__(self, file_path) -> None:
        """Initializes ConllDataset object.

        Args:
            file_path (str): Path to the data file.
        """
        super().__init__()
        self._file_path = file_path

    def load_data(self) -> List[Sample]:
        """Loads data from a CoNLL file.

        Returns:
            list: List of sentences in the dataset.
        """
        data = []
        with open(self._file_path) as f:
            content = f.read()
            docs_strings = re.findall(r"-DOCSTART- \S+ \S+ O", content.strip())
            docs = [i.strip() for i in re.split(r"-DOCSTART- \S+ \S+ O", content.strip()) if i != '']
            for d_id, doc in enumerate(docs[:5]):
                #  file content to sentence split
                sentences = doc.strip().split('\n\n')

                if sentences == ['']:
                    data.append(([''], ['']))
                    continue

                for sent in sentences:
                    # sentence string to token level split
                    tokens = sent.strip().split('\n')

                    # get annotations from token level split
                    token_list = [t.split() for t in tokens]

                    #  get token and labels from the split
                    ner_labels = []
                    cursor = 0
                    for split in token_list:
                        ner_labels.append(
                            NERPrediction.from_span(
                                entity=split[-1],
                                word=split[0],
                                start=cursor,
                                end=cursor + len(split[0]),
                                doc_id=d_id,
                                doc_name=(docs_strings[d_id] if len(docs_strings) > 0 else '') ,
                                pos_tag=split[1],
                                chunk_tag=split[2]
                            )
                        )
                        cursor += len(split[0]) + 1  # +1 to account for the white space

                    original = " ".join([label.span.word for label in ner_labels])

                    data.append(
                            Sample(original=original, expected_results=NEROutput(predictions=ner_labels))
                        )

        return data

    def export_data(self, data: List[Sample], output_path: str):
        temp_id = None
        text = ""
        for i in data:
            test_case = i.test_case
            original = i.original
            if test_case:
                test_case_items = test_case.split()
                # original_items = original.split()
                norm_test_case_items = test_case.lower().split()
                norm_original_items = original.lower().split()
                # if len(test_case_items) == len(original_items):
                for jdx, item in enumerate(norm_test_case_items):
                    # print(item, norm_original_items)
                    if item in norm_original_items:
                        oitem_index = norm_original_items.index(item)
                        j = i.expected_results.predictions[oitem_index]
                        if temp_id != j.doc_id and jdx == 0:
                            text += f"{j.doc_name}\n\n"
                            temp_id = j.doc_id
                        else:
                            text+=f"{test_case_items[jdx]} {j.pos_tag} {j.chunk_tag} {j.entity}\n"
                        norm_original_items.pop(oitem_index)
                    else:
                        text+=f"{test_case_items[jdx]} {j.pos_tag} {j.chunk_tag} O\n"
                text+="\n"
               
            else:
                for j in i.expected_results.predictions:
                    if temp_id != j.doc_id:
                        text += f"{j.doc_name}\n\n"
                        temp_id = j.doc_id
                    else:
                        text+=f"{j.span.word} {j.pos_tag} {j.chunk_tag} {j.entity}\n"
                text+="\n"
        with open(output_path, "wb") as fwriter:
            fwriter.write(bytes(text, encoding="utf-8"))



class JSONDataset(_IDataset):
    """Class to handle JSON dataset files. Subclass of _IDataset.
    """

    def __init__(self, file_path) -> None:
        """Initializes JSONDataset object.

        Args:
            file_path (str): Path to the data file.
        """
        super().__init__()
        self._file_path = file_path

    def load_data(self):
        pass

    def export_data(self):
        pass


class CSVDataset(_IDataset):
    """Class to handle CSV files dataset. Subclass of _IDataset.
    """

    def __init__(self, file_path) -> None:
        """Initializes CSVDataset object.

        Args:
            file_path (str): Path to the data file.
        """
        super().__init__()
        self._file_path = file_path

    def load_data(self) -> pd.DataFrame:
        """Loads data from a csv file.

        Returns:
            pd.DataFrame: Csv file as a pandas dataframe.
        """
        return pd.read_csv(self._file_path)
    
    def export_data(self):
        pass
