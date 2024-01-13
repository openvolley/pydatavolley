import sys

if sys.version_info[0] == 3:
    str_types = str
    is_py27 = False
else:
    str_types = (str, unicode)  # NOQA
    is_py27 = True
