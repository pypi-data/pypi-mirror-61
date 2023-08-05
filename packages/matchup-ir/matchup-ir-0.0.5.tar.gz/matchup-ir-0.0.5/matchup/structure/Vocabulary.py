"""
    Describes the data structure of IR models design.
"""
from os import path, listdir
from collections import defaultdict
from typing import List

import pickle

from matchup.structure.Occurrence import Occurrence
from matchup.structure.weighting.Idf import IDF
from matchup.structure.weighting.Tf import TF

from matchup.presentation.Sanitizer import Sanitizer
from matchup.presentation.Text import Term
from matchup.presentation.formats.File import ExtensionNotSupported, File

LIB_PATH = path.abspath("./static/lib")
SAVED_FILE_NAME = 'collection.bin'


class Vocabulary:

    def __init__(self, save, **kwargs):
        """
        :param response: Path to save processed Vocabulary
        :param kwargs: only accepts 'stopwords', with the stopwords file path
        """
        self._inverted_file = defaultdict(list)
        self._idfs = None
        self._tfs = None
        self.file_names = set()
        self.max_frequency_map = defaultdict(float)
        self._collection_path = self.__make_prefix(save) + f"/{SAVED_FILE_NAME}"
        self._sanitizer = self.__make_sanitizer(**kwargs)

    def import_file(self, file_path: str) -> bool:
        """
            Given a file path of a document, this function append this document into some structure, case the path are
            correct. The processing of this file can be started running function generate_collection()

        :param file_path: string that represents a relative or absolute path of an txt file
        :return: boolean flag that indicates if the file has been identified
        """
        if path.exists(file_path):
            self.file_names.add(file_path)
            return True
        return False

    def import_folder(self, folder_path: str, *, update_path: bool = False) -> bool:
        """
            Generalization of import_file(). This function receive a folder path and try to append all documents of
            this folder into some structure. he processing of all this file can be started running function
             generate_collection()

        :param folder_path: string that represents a relative or absolute path of an folder
        :param update_path: flag to update processed file path
        :return: boolean flag that indicates if the folder has been identified
        """
        if path.isdir(folder_path):
            list_dir = filter(lambda x: f'{SAVED_FILE_NAME}' not in x, listdir(folder_path))
            for filename in list_dir:
                self.import_file(folder_path + "/" + filename)
            if update_path:
                self._collection_path = folder_path + f"/{SAVED_FILE_NAME}"
            return True
        raise FileNotFoundError

    def import_collection(self) -> bool:
        """
            This is a function that recover the vocabulary previously generated.
        :return: boolean flag that indicates success or failure in case the vocabulary has no generated yet.
        """
        self._inverted_file.clear()
        if path.exists(self._collection_path):
            with open(self._collection_path, mode='rb') as file:
                self._inverted_file = pickle.load(file)
                self.__retrieve_file_names()
            return True
        raise FileNotFoundError

    def generate_collection(self) -> None:
        """
            This function try to process all content of files that have been inserted before, generating
            the vocabulary data structure ready for use.
        :return: None
        """
        for file_name in self.file_names:
            file = None
            try:
                file = File.open(file_name)
                content_file = File.content_file(file_name, file)
                self.__process_file(file_name, content_file)
            except ExtensionNotSupported:
                continue
            finally:
                File.close(file)

    def save(self) -> bool:
        """
            Persist data structure on disc.
        :return: boolean flag that indicates if the data structure can be persisted.
        """
        self.__sort()
        if self._inverted_file:
            with open(self._collection_path, mode='wb') as file:
                pickle.dump(self._inverted_file, file)
            return True
        raise ReferenceError

    def size_vocabulary(self) -> int:
        """
            Get the number of words this data structure almost process
        :return: Size of data structure vocabulary
        """
        return len(self._inverted_file)

    @property
    def stopwords_path(self) -> str:
        """
        :return: Get the absolute path that stop words are persisted.
        """
        return self._sanitizer.stopwords_path

    @stopwords_path.setter
    def stopwords_path(self, stp_path: str) -> None:
        """
        :return: Get the absolute path that stop words are persisted.
        """
        self._sanitizer.stopwords_path = stp_path

    @property
    def idf(self) -> IDF:
        """
            Get the data structure that represents the IDF weithing
        :return: IDF object
        """
        return self._idfs

    @idf.setter
    def idf(self, idf: IDF) -> None:
        """
            This function just calculate IDF of all keywords on vocabulary
        :return: None
        """
        self._idfs = idf
        self._idfs.generate(self)

    @property
    def tf(self) -> TF:
        """
            Get the data structure that represents the TF weithing
        :return: TF object
        """
        return self._tfs

    @tf.setter
    def tf(self, tf: TF) -> None:
        """
            Set the data structure that represents the TF weithing
        :param tf: TF Object
        :return: None
        """
        self._tfs = tf

    @property
    def keys(self) -> list:
        """
            Get all keywords presents in vocabulary
        :return: list of all keywords
        """
        return list(self._inverted_file.keys())

    @property
    def sanitizer(self) -> "Sanitizer":
        return self._sanitizer

    def get_number_docs_by_keyword(self, kw: str) -> int:
        """
            Get the number of documents contains some keyword
        :param kw: string that represents some keyword
        :return: number of documents
        """
        return len(self._inverted_file[kw])

    def __str__(self) -> str:
        """
            Transform an Vocabulary object in an String
        :return: String that represents the structure of vocabulary
        """
        vocabulary = ""
        for key in self._inverted_file.keys():
            vocabulary += str(key + ":" + str(self._inverted_file[key]) + "\n")
        return vocabulary

    def __contains__(self, item: str) -> bool:
        """
            This function enables the user to make the associative operation with 'in'
        :param item: keyword
        :return: boolean flag that return true if the keyword are in vocabulary
        """
        return item in self._inverted_file

    def __getitem__(self, item: str) -> List[Occurrence]:
        """
            Get some vocabulary occurrences by item, or instantiante it on data structure
        :param item: keyword
        :return: Occurrences of keyword
        """
        return self._inverted_file[item]

    def __push(self, terms: List[Term], file_name: str) -> None:
        """
            Auxiliar function that push all file terms in vocabulary
        :param terms: list with all file terms
        :param file_name: path of file
        :return: None
        """
        for term in terms:
            try:
                idx = self._inverted_file[term.word].index(file_name)
                occurrence = self._inverted_file[term.word][idx]
                occurrence.add(position=term.position)

                if self.max_frequency_map[file_name] < occurrence.frequency:
                    self.max_frequency_map[file_name] = occurrence.frequency

            except ValueError:
                occurrence = Occurrence(file_name, term)
                self._inverted_file[term.word].append(occurrence)

                if self.max_frequency_map[file_name] < occurrence.frequency:
                    self.max_frequency_map[file_name] = occurrence.frequency

    def __sort(self) -> None:
        """
            Order the documents in vocabulary structure.
        :return: None
        """
        for key in self._inverted_file:
            self._inverted_file[key] = sorted(self._inverted_file[key], key=Occurrence.doc)

    def __retrieve_file_names(self) -> None:
        """
            Iterate the data structure retrieving the file names that generated it vocabulary
        :return: None
        """
        for keyword in self._inverted_file:
            for occurrence in self._inverted_file[keyword]:
                self.file_names.add(occurrence.doc())
                if self.max_frequency_map[occurrence.doc()] < occurrence.frequency:
                    self.max_frequency_map[occurrence.doc()] = occurrence.frequency

    def __process_file(self, filename, content_file):
        number_line = 1
        for content_line in content_file:
            terms = self._sanitizer.sanitize_line(content_line, number_line)
            self.__push(terms, filename)
            number_line += 1

    @classmethod
    def __make_sanitizer(cls, **kwargs) -> Sanitizer:
        stopwords = kwargs.get("stopwords")
        if stopwords:
            return Sanitizer(stopwords_path=stopwords)
        else:
            return Sanitizer()

    @classmethod
    def __make_prefix(cls, save):
        return save if save else LIB_PATH

