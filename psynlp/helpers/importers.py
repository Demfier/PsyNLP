import time
import operator

from ..core import oracle
from .text import iterLCS
from ..core.fca import FCA
from .misc import deterministic_pac


def fetch_testing_data(language='english'):
    """
    Fetches testing data given a language
    Parameters:
    -----------------------------------
    language : str
        Name of the language whose testing data to fetch

    Returns:
    -----------------------------------
    T : list[tuple]
        List of tuples from the testing dataset of the language sorted
        alphabetically
    """
    filepath = "psynlp/data/{}-dev".format(language)
    T = []
    file = open(filepath, 'r')
    for line in file.readlines():
        source, expected_dest, metadata = line.split("\t")
        if "*" not in source and "*" not in expected_dest:
            metadata = metadata.strip("\n")
            T.append((source, metadata, expected_dest))
    verbose_print_1("Providing all test words in structured manner")
    T = sorted(T, key=operator.itemgetter(0))
    return T


def parse_metadata_words(language='english', quality='low'):
    """
    Identifies words corresponding to different metadata in the language
    Parameters:
    -----------------------------------
    language : str
        Name of the language whose testing data to fetch
    quality : str
        size of the dataset to consider

    Returns:
    -----------------------------------
    metadata_words : dict
        A dictionary with all the words grouped by metadata
    """
    metadata_words = {}
    filepath = "psynlp/data/{}-train-{}".format(language, quality)
    file = open(filepath, 'r')
    for line in file.readlines():
        source, dest, metadata = line.split("\t")
        if "*" not in source and "*" not in dest:
            metadata = metadata.strip()
            if metadata in metadata_words:
                metadata_words[metadata].append((source, dest))
            else:
                metadata_words[metadata] = []
    return metadata_words


def parse_metadata_fca(metadata_words, cluster_type='pac'):
    """
    Computes PAC-basis based on the different metadata in language
    Parameters:
    -----------------------------------
    metadata_words : dict
        A dictionary with all the words grouped by metadata
    cluster_type : str
        clustering algo to use while grouping

    Returns:
    -----------------------------------
    metadata_fca : dict
        A dictionary with canonical-basis computed for each of the metadata
        group in the language
    """
    metadata_fca = {}
    for metadata in metadata_words:
        wordpairs = metadata_words[metadata]
        concept = init_concept_from_wordpairs(wordpairs)
        if len(concept.objects()) > 0:
            start1 = time.clock()
            if cluster_type == 'pac':
                pac = concept.pac_basis(oracle.is_member, 1.0, 1.0)
            else:
                pac = deterministic_pac(concept)
            end1 = time.clock() - start1
        else:
            pac, end1 = None, None
        metadata_fca[metadata] = (concept, pac, end1)
    return(metadata_fca)


def fetch_input_output_pairs(language='english', quality='low'):
    """
    Fetches input-output examples from training dataset of the given language
    Parameters:
    -----------------------------------
    language : str
        Name of the language whose testing data to fetch
    quality : str
        size of the dataset to consider

    Returns:
    -----------------------------------
    T : list[tuple]
        List of tuples from the training dataset of the language sorted
        alphabetically
    """
    filepath = "psynlp/data/{}-train-{}".format(language, quality)
    T = list()
    file = open(filepath, 'r')
    for line in file.readlines():
        source, dest, metadata = line.split("\t")
        if "*" not in source and "*" not in dest:
            metadata = metadata.strip("\n").split(";")
            T.append((source, metadata, dest))
    verbose_print_1("Providing all words in structured manner, to OSTIA")
    T = sorted(T, key=operator.itemgetter(0))
    return T


def init_concept_from_wordpairs(wordpairs):
    """
    Initializes a concept from a given set of input-output examples by adding
    relations.
    Parameters:
    -----------------------------------
    wordpairs : list[tuple]
        List of input output examples

    Returns:
    -----------------------------------
    concept : object[FCA]
        Initialized concept
    """
    concept = FCA()
    for (source, target) in wordpairs:
        if "*" not in source and "*" not in target:
            mutations = iterLCS({'source': source, 'target': target})
            for addition in mutations['added']:
                concept.add_relation("insert_"+addition, source)
            for deletion in mutations['deleted']:
                concept.add_relation("delete_"+deletion, source)
    return(concept)
