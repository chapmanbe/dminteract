from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
import numpy as np
from skimage.io import imshow, imread
import os
import pydicom
import pandas as pd
from .. import eval as _e
import ipywidgets as widgets
import altair as alt


from ipywidgets import interact
def get_tags(mod):
    import sqlite3 as sq
    conn = sq.connect(os.path.join(_e.__DBDIR__,mod+".sqlite"))
    c = conn.cursor()
    c.execute("""SELECT tags FROM dmquestions""")
    tags = [t[0] for t in c.fetchall()]
    return tags

_tags = get_tags("m4")
_m4c_groups = ['qbank1', 'qbank2', 'qbank3', 'qbank4']
_m4c_evals = {key:[t for t in _tags if key in t] for key in _m4c_groups}

__scores = {key:{} for key in _m4c_evals.keys()}

del _tags

def get_img_metadata(fname):
    parser = createParser(fname)
    with parser:
        try:
            metadata = extractMetadata(parser)
        except Exception as err:
            print("Metadata extraction error: %s" % err)
            metadata = None
    if not metadata:
        print("Unable to extract metadata")
        return None
    return metadata


def view_img_metadata(f):
    metadata = get_img_metadata(f)
    return "\n".join([line for line in metadata.exportPlaintext()])

def win_lev(img, w, l, maxc=255):
    """
    Window (w) and level (l) data in img
    img: numpy array representing an image
    w: the window for the transformation
    l: the level for the transformation
    maxc: the maximum display color
    """

    m = maxc/(2.0*w)
    o = m*(l-w)
    return np.clip((m*img-o),0,maxc).astype(np.uint8)

def view_dicom_data(img, group, elem):
    try:
        g = int(group,base=16)
        e = int(elem, base=16)
        tmp = img[(g, e)]
        print ("%s :-> %s"%(tmp.name, tmp.value))
    except:
        print()

def view_chest(img,w,l):
    imshow(win_lev(chest.pixel_array, w, l), cmap="gray")

def view_volume(img,s, w, l):
    imshow(win_lev(liver.pixel_array[s,:,:],w,l))

def get_rev_dict(di):
    return dict([(e.name,e.tag) for e in di.values()])
def view_dicom_data_rev(img, item):
    try:
        tmp = img[item]
        print ("(%s, %s) :-> %s"% (hex(item.group), hex(item.elem),tmp.value))
    except Exception as error:
        print(error)
        print()

def get_img_histo(img, win=None, nbins=100):

    idata = img.pixel_array.flatten()
    label = "Pixel Values: %s= %s (%+4d - %+4d)"%(img[(0x008, 0x0060)].name,
                                                         img[(0x008, 0x0060)].value,
                                                         np.min(idata), np.max(idata))
    if win == None:
        win = [np.min(idata), np.max(idata)]
    tmp = np.extract((idata >=win[0])& (idata <=win[1]), idata)
    hist, bin_edges = np.histogram(tmp, bins=nbins)
    data = pd.DataFrame({label:bin_edges[:-1],
                         "count":hist})
    return alt.Chart(data).mark_bar().encode(
                 x=label,
                 y='count').properties(width=256, height=256)





def get_examine_dicom_widget(imgs, allmin, allmax):
    img_select = widgets.Dropdown(options=imgs.items(),
                             layout=widgets.Layout(width="256px"))

    win_select = widgets.IntRangeSlider(value=[allmin, allmax],
                                        max=allmax,
                                        min=allmin,
                                       layout=widgets.Layout(width="300px"))

    a = interact(get_img_histo,img=img_select, win=win_select, nbins=50)
    a.widget.layout = widgets.Layout(width="375px")
    win = widgets.IntSlider(value=500, min=1, max=5000)
    lev = widgets.IntSlider(values=500, min=allmin, max=allmax)
    iow = widgets.Output(layout=widgets.Layout(width="300px"))

    def view_img(img, w, l):
        iimg = img.pixel_array
        with iow:
            imshow(win_lev(iimg, w, l), cmap="gray")

    b = interact(view_img, img=img_select, w=win, l=lev)
    b.widget.layout = widgets.Layout(width='375px')
    return widgets.HBox([b.widget, a.widget])




question_banks = {key:{tag:_e.create_question_widget("m4", tag) for tag in _m4c_evals[key]}
                     for key in _m4c_evals.keys() }
