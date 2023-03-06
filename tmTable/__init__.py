import sys, os

UTM_XSD_DIR =  os.path.join(os.path.dirname(__file__), 'xsd')
os.environ.setdefault('UTM_XSD_DIR', UTM_XSD_DIR)

from .tmTable import *

from .version import __version__
