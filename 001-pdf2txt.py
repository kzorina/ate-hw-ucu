#!/usr/bin/env python2
#encoding: UTF-8

# reads pdf files from directory
import ConfigParser
import ate

from os import listdir
from os.path import isfile, join, isdir

config = ConfigParser.ConfigParser()
config.readfp(open('config.ini'))

pdf_dir=config.get('main', 'pdf_dir')
txt_dir=config.get('main', 'txt_dir')

pdf_files=sorted([ (pdf_dir, f) for f in listdir(pdf_dir) if isfile(join(pdf_dir, f)) and f.lower().endswith(".pdf")])

print pdf_files
for f in pdf_files:
    fpath_out=join(txt_dir, f[1][:-4]+'.txt')
    print pdf_dir,'/',f[1],"=>", fpath_out
    ftxt = open(fpath_out,'w')
    ftxt.write(ate.pdf2text(join(f[0], f[1])).replace("\n"," "))
    ftxt.close()
