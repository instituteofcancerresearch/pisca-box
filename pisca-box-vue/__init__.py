import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
print(dir_path,parent_dir_path)
sys.path.insert(0, dir_path)