
import sys
import json
import subprocess

from quarto.quarto import find_quarto

def metadata(input):
  args = ["metadata", input, "--json"]
  metadata_json = subprocess.check_output([find_quarto()] + args)
  return json.loads(metadata_json)

 
