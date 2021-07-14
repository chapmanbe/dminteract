import sys
sys.path.append("../../")
import dminteract
import dminteract.eval as _e
import os
import sqlite3 as sq
import pandas as pd

_e.__DBDIR__ = "/Users/brian/Code/Melbourne/dminteract_instructor/dbs"


dbname = os.path.join(_e.__DBDIR__, "m4.sqlite")
conn = sq.connect(dbname)
pd.read_sql("""SELECT name FROM sqlite_master WHERE type='table'""", conn)
questions = pd.read_sql("""SELECT * FROM dmquestions""", conn)

_e.create_question_widget("m4", "photo1, qbank1")
_e.create_question_widget("m4", "dd3, qbank3") 


