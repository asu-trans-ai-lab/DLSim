# -*- coding:utf-8 -*-
##############################################################
# Created Date: Friday, April 21st 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

import os
import datetime
from pathlib import Path
from typing import Union  # Python version <= 3.9
import ctypes
import platform
from pyufunc import path2linux


def check_required_files_exist(required_files: list, dir_files: list) -> bool:
    # format the required file name to standard linux path
    required_files = [path2linux(os.path.abspath(filename)) for filename in required_files]

    required_files_short = [filename.split("/")[-1] for filename in required_files]
    dir_files_short = [filename.split("/")[-1] for filename in dir_files]

    # mask have the same length as required_files
    mask = [file in dir_files_short for file in required_files_short]
    if all(mask):
        return True

    print(f"Error: Required files are not satisfied, \
          missing files are: {[required_files_short[i] for i in range(len(required_files_short)) if not mask[i]]}")

    return False


def load_cpp_shared_library():
    _os = platform.system()
    if _os.startswith('Windows'):
        _dtalite_dll = os.path.join(os.path.dirname(__file__), 'pydtalite_bin/DTALite.dll')
    elif _os.startswith('Linux'):
        _dtalite_dll = os.path.join(os.path.dirname(__file__), 'pydtalite_bin/DTALite.so')
    elif _os.startswith('Darwin'):
        # check CPU is Intel or Apple Silicon
        if platform.machine().startswith('x86_64'):
            _dtalite_dll = os.path.join(os.path.dirname(__file__), 'pydtalite_bin/DTALite_x86.dylib')
        else:
            _dtalite_dll = os.path.join(os.path.dirname(__file__), 'pydtalite_bin/DTALite_arm.dylib')
    else:
        raise Exception('Please build the shared library compatible to your OS \
                        using source files')

    _dtalite_engine = ctypes.cdll.LoadLibrary(_dtalite_dll)

    _dtalite_engine.network_assignment.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
    return _dtalite_engine
