
import os
import sys
import shutil
import subprocess

def path():
  path_env = os.getenv("QUARTO_PATH")
  if path_env is None:
    return shutil.which("quarto")
  else:
    return path_env
  

def find_quarto():
  quarto = path()
  if quarto is None:
    raise FileNotFoundError('Unable to find quarto command line tools.')
  return quarto
