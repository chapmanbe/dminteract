import sqlite3 as sq
import ipywidgets as widgets
from ipywidgets import interact
from IPython.display import clear_output
import os

__PERMISSIVE__ = True
__DBDIR__ = os.path.join(os.path.abspath(os.path.dirname(__file__)), ".dbs")
_m4c_evals = {"basic_image_standards":["simg1", "simg2", "simg3", "simg4"],
              "dicom_intro":["dd1", "dd2", "dd3", "dd4", "dd5", "dd6"]}

def create_question_widget(mod, tag):
    conn = sq.connect(os.path.join(__DBDIR__,mod+".sqlite"))
    cursor = conn.cursor()
    cursor.execute("""SELECT
                      dmquestions.rowid,
                      dmquestions.question,
                      questiontype.type
                  FROM
                      dmquestions INNER JOIN
                          questiontype ON dmquestions.type=questiontype.rowid
                   WHERE tags = ?""",(tag,))
    q0 = cursor.fetchone()


    cursor.execute("""SELECT
                         answer, status, feedback
                      FROM
                         dmanswers
                      WHERE
                         dmanswers.qid=?""",(q0[0],))
    answers = cursor.fetchall()


    radio_options = [(a[0], i) for i, a in enumerate(answers)]

    alternativ = widgets.RadioButtons(
        options = radio_options,
        description = '',
        disabled = False
    )

    description_out = widgets.Output()
    with description_out:
        print(q0[1])

    feedback_out = widgets.Output()

    def check_selection(b):
        a = int(alternativ.value)
        if answers[a][1]:
            s = '\x1b[6;30;42m' + "correct: %s"%answers[a][2] + '\x1b[0m' +"\n" #green color
        else:
            s = '\x1b[5;30;41m' + "incorrect: %s"%answers[a][2] + '\x1b[0m' +"\n" #red color
        with feedback_out:
            feedback_out.clear_output()
            print(s)
        return

    check = widgets.Button(description="submit")
    check.on_click(check_selection)


    return widgets.VBox([description_out, alternativ, check, feedback_out])
