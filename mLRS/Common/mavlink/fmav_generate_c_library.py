#!/usr/bin/env python
'''
fmav_generate_c_library.py
calls fastMavlink generator for C header files
Copyright (c) OlliW, OlliW42, www.olliw.eu
'''
import os
import shutil
import re
import sys

from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'tools'))
from setup_cleanup import reset_generated_dir

os.chdir(os.path.dirname(os.path.abspath(__file__)))


#options to set

mavlinkpathtorepository = os.path.join('..','..','modules','fastmavlink')

mavlinkdialect = "mlrs_all.xml"

mavlinkoutputdirectory = 'out'


'''
Imports
'''
sys.path.insert(0,mavlinkpathtorepository)

from generator import fmav_gen as mavgen
from generator.modules import fmav_flags as mavflags

'''
Generates the header files and place them in the output directory.
'''

outdir = mavlinkoutputdirectory
xmlfile = mavlinkdialect

print('----------')
print('kill out dir')
reset_generated_dir(Path(__file__).resolve().parent / outdir)
print('----------')

opts = mavgen.Opts(outdir, parse_flags=mavflags.PARSE_FLAGS_WARNING_ENUM_VALUE_MISSING)
args = [xmlfile]
try:
    mavgen.fmavgen(opts,args)
    print('Successfully Generated Headers', 'Headers generated successfully.')

except Exception as ex:
    exStr = str(ex)
    print('Error Generating Headers','{0!s}'.format(exStr))
    sys.exit(1)

