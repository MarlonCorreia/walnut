"""
Walnut Utils
"""

###
# Libraries
###

import os
import shutil
from urllib import request



###
# Utils
###

def create_dir(dir):
    os.mkdir(dir)

def delete_dir(dir):
    shutil.rmtree(dir)

def get_file_size(url):
    req = request.Request(url, method='HEAD')
    f = request.urlopen(req)
    if f.status == 200:
        m_size = _bytesto(f.headers.get('Content-Length', 0), 'm')
        return m_size

def _bytesto(bytes, to, bsize=1024): 
    """
    Bytes convertion
    Thanks: https://gist.github.com/shawnbutts/3906915#gistcomment-3389096
    """

    a = {'k' : 1, 'm': 2, 'g' : 3, 't' : 4, 'p' : 5, 'e' : 6 }
    r = float(bytes)
    return r / (bsize ** a[to])

