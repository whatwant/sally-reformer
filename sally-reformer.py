#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import sys
import argparse
import codecs
import platform
import locale
import shutil
import pprint

reload(sys)
sys.setdefaultencoding('utf-8')



INFO = {
    'PATH'           : {},
    'PYTHON_VERSION' : '',
    'PATTERN'        : {},
    'FILEPATH'       : {},
    'ENCODING'       : ''
    }
    



    
if __name__ == "__main__":


    ##### [Get argvs] #####
    parser = argparse.ArgumentParser(description="This code is written for rename filename with pattern")
    parser.add_argument("-p", "--pattern", dest="pattern_filepath", action="store", default="pattern.csv", help="pattern filepath", required=True)
    parser.add_argument("-s", "--source", dest="source_directory", action="store", default="./", help="source directory", required=False)
    args = parser.parse_args()
    
    if not os.path.isfile( args.pattern_filepath ):
        print( "[error] file not exist : %s" % args.pattern_filepath )
        sys.exit(1)

    INFO['PATH']['pattern_filepath'] = args.pattern_filepath
    print( "[info] file check '%s' (ok)" % INFO['PATH']['pattern_filepath'] )

    
    if not os.path.isdir( args.source_directory ):
        print( "[error] directory not exist : %s" % args.source_directory )
        sys.exit(1)
    
    INFO['PATH']['source_directory'] = args.source_directory
    print( "[info] directory check '%s' (ok)" % INFO['PATH']['source_directory'] )
    
    
    
    
    
    ##### [Python version check] #####
    MIN_PYTHON_VERSION = (2, 7)      # minimum supported python version
    MAX_PYTHON_VERSION = (2, 8)      # maximum supported python version
    
    ver = sys.version_info
    if (((ver[0], ver[1]) < MIN_PYTHON_VERSION) or ((ver[0], ver[1]) > MAX_PYTHON_VERSION)):
        print( "[error] Python version %s unsupported.\nPlease use Python 2.6 - 2.7 instead." % sys.version.split(' ')[0] )
        sys.exit(1)
    
    INFO['PATHON_VERSION'] = sys.version.split(' ')[0]
    print( "[info] python version check '%s' (ok)" % INFO['PATHON_VERSION'] )
    
    
    
    
    
    ##### [OS check] #####
    if not platform.system() in ['Windows']:
        print( "[error] This script execute only under Windows. But, this env in %s" % platform.platform() )
        sys.exit(1)
    
    print( "[info] Operating System check '%s' (ok)" % platform.platform() )
    
    
    
    
    
    ## Locale Temp Code
    #loc = locale.getdefaultlocale()
    #if loc[1]:
    #    encoding = loc[1]
    
    
    
    
    
    ##### [Encoding check] #####
    INFO['ENCODING'] = sys.stdout.encoding
    
    ##TODO: more check about None case
    if INFO['ENCODING'] == None:
        INFO['ENCODING'] = 'cp949'
    #sys.stdin.encoding
    
    
    
    
    
    ##### [Load Pattern] #####
    with codecs.open(INFO['PATH']['pattern_filepath'], 'r', 'utf-8') as fp:
        line = fp.readline()
        while line:
            item = line.split(",")
            if (len(item) != 2):
                print( "[warning] wrong pattern line: %s" % line )
                continue
            
            item[1] = item[1].strip()
            if (item[1] in INFO['PATTERN'].keys()):
                print( "[warning] duplicated pattern: %s" % item[1] )
                continue
            
            item[0] = item[0].strip()
            INFO['PATTERN'][ item[1] ] = item[0]

            line = fp.readline()

    print( "[info] load pattern count (%s)" % len(INFO['PATTERN']) )
    ##TODO: pattern file rewrite
    
    
    
    
    
    ##### [Load FilePath] #####
    for dirpath, dirnames, filenames in os.walk(INFO['PATH']['source_directory']):
        dirpath = dirpath.decode( INFO['ENCODING'] ).encode('utf8')
        for filename in filenames:
            filename = filename.decode( INFO['ENCODING'] ).encode('utf8')
            INFO['FILEPATH'][ os.path.join(dirpath, filename) ] = {
                'DIR'       : dirpath,
                'FILENAME'  : filename,
                'FIRSTNAME' : filename.split(".")[0],
                'LASTNAME'  : ".".join( filename.split(".")[1:] )
                }
            
    print( "[info] load filepath count (%s)" % len(INFO['FILEPATH']) )
    
    
    
    
    
    ##### [Matching Pattern] #####
    RESULT = []
    for idx, (filepath, items) in enumerate(INFO['FILEPATH'].items()):
    
        print items['FILENAME'].decode('utf8'), "(", items['FIRSTNAME'].decode('utf8'), ")", ":",
        for pattern in INFO['PATTERN'].keys():
            if pattern == items['FIRSTNAME']:
            
                ITEM = {
                    'DIR'  : items['DIR'],
                    'FROM' : items['FILENAME'],
                    'TO'   : INFO['PATTERN'][ pattern ] + "." + items['LASTNAME']
                }
                print ITEM['TO'].decode( 'utf8' ),
                
                
                src = os.path.basename( os.path.normpath( ITEM['DIR'].decode( 'utf8' ) ) )
                dst = ITEM['TO'].decode( 'utf8' )
                
                if( src == dst ):
                    src = ITEM['DIR'].decode( 'utf8' )
                    dst = ".".join(ITEM['DIR'].split(".")[:-1]).decode('utf8')
                    
                    os.rename( src, dst )
                    ITEM['DIR'] = ".".join(ITEM['DIR'].split(".")[:-1])
                
                src = os.path.join( ITEM['DIR'], ITEM['FROM'] ).decode( 'utf8' )
                dst = os.path.join( INFO['PATH']['source_directory'], ITEM['TO'] ).decode( 'utf8' )
                
                shutil.move( src, dst)
                if os.listdir( ITEM['DIR'].decode( 'utf8' ) ) == []:
                    shutil.rmtree( ITEM['DIR'].decode( 'utf8' ) )
                
                #print
                #print os.path.join( ITEM['DIR'], ITEM['FROM'] ).decode( 'utf8' )
                #print os.path.join( INFO['PATH']['source_directory'], ITEM['TO'] ).decode( 'utf8' )
                #print
                
                
                break
    
        print

        
    sys.exit()