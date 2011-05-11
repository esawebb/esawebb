#
# -*- coding: utf-8 -*-
#
# eso.org
# Copyright 2011 ESO
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Dirk Neumayer <dirk.neumayer@gmail.com>
#
#   script to test and apply functions in hubblesite/avm.py
#   
#*************************************************************************************************************

from spacetelescope.hubblesite import avm
import os, sys
import logging
logger = logging.getLogger(__name__)

def prepare4unicode():
    import sys, codecs, locale
    #this allows stdout > into a file
    sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)
    #little unicode test
    star = unichr(9734)
    print star
    return 

if __name__ == '__main__':
    # for testing
    logging.basicConfig()
    prepare4unicode()
    
    script_path = os.path.dirname(sys.argv[0])
    json_file = os.path.join(script_path, 'stpr_search.json')
    
    data = avm.load_json(json_file)
    for dataset in data:
        avmdict = avm.jsondict2avmdict(dataset)
        if avmdict:
            for key in avmdict.keys():
                print "%-30s: %s" % (key, avmdict[key])
        

            
        
            

                         



