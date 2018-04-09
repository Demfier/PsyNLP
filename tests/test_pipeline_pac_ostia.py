import pytest
from ..psynlp.pipelines import pac_ostia


def test_fetch_accuray():
    print(pac_ostia.fetch_accuracy(language='bengali', quality='low'))
