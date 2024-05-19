import os
import sys

cur_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, cur_dir)

os.environ['MPLCONFIGDIR'] = '/var/www/.config/matplotlib'

from app import app as application
