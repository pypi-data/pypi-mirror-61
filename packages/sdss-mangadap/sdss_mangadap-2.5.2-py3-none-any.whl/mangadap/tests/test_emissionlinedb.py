
import pytest
import os

from IPython import embed

from mangadap.par.emissionlinedb import EmissionLineDB

import warnings
warnings.simplefilter("ignore", UserWarning)
warnings.simplefilter("ignore", RuntimeWarning)

def test_read():
    dbs = EmissionLineDB.available_databases()
    assert len(dbs) > 0, 'No emission-line databases available'
    for key in dbs.keys():
        emldb = EmissionLineDB.from_key(key)

def test_mpl9():
    emldb = EmissionLineDB.from_key('ELPMPL9')
    assert len(emldb) == 35, 'Incorrect number of emission lines'
    assert 'ArIII' in emldb['name'], 'Does not contain ArIII in list'

