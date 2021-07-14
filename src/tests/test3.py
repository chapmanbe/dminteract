import sys
sys.path.append("../../")
import dminteract
import dminteract.eval as _e
import os
import sqlite3 as sq
import pandas as pd

_e.__DBDIR__ = "/Users/brian/Code/Melbourne/dminteract_instructor/dbs"


from dminteract.modules.m4c import *
from dminteract.modules.m4c import _m4c_evals
print(_m4c_evals)
