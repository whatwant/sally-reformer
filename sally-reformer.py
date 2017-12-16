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
    'FILEPATH'       : [],
    'ENCODING'       : ''
    }
    

    
class TFile:
    
    def __init__(self, dirpath, filename):
        self.dirpath   = dirpath
        self.filename  = filename
        self.firstname = filename.split(".")[0]
        self.lastname  = ".".join( filename.split(".")[1:] )
    

    def equalsFirstname(self, firstname):
        return True if( self.firstname == firstname ) else False
    

    def getFilename(self, decoding=''):
        result = self.filename
    
        if( decoding in ['utf8', 'utf-8'] ):
            result = self.filename.decode('utf8')

        return result


    def getFirstname(self, decoding=''):
        result = self.firstname
    
        if( decoding in ['utf8', 'utf-8'] ):
            result = self.firstname.decode('utf8')

        return result


    def getLastname(self, decoding=''):
        result = self.lastname
    
        if( decoding in ['utf8', 'utf-8'] ):
            result = self.lastname.decode('utf8')

        return result
    
    
    def getDirpath(self, decoding=''):
        result = self.dirpath
    
        if( decoding in ['utf8', 'utf-8'] ):
            result = self.dirpath.decode('utf8')

        return result
    
    
    def isExistedFilename(self, dirpath, filename):
        filenames = os.listdir( dirpath )

        return True if( filename in filenames ) else False


    def getNonexistantFilename(self, dirpath, new_filename):

        i = 0
        while self.isExistedFilename(dirpath, new_filename):
            filename, extension = os.path.splitext(new_filename)

            i += 1
            new_filename = "{}-{}{}".format(filename, i, extension)
    
        return new_filename
    
    
    def renameFilename(self, new_dirpath, new_filename):
        old_filepath = os.path.join( self.dirpath, self.filename ).decode( 'utf8' )
        
        new_filename = self.getNonexistantFilename( new_dirpath, new_filename )
        new_filepath = os.path.join( new_dirpath, new_filename ).decode( 'utf8' )
        
        os.rename( old_filepath, new_filepath )
        
        self.dirpath   = dirpath
        self.filename  = new_filename
        self.firstname = new_filename.split(".")[0]
        
        return True
        


        
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
            
            INFO['FILEPATH'].append( TFile(dirpath, filename) )

    print( "[info] load filepath count (%s)" % len(INFO['FILEPATH']) )
    print
    
    
    
    ##### [Matching Pattern] #####
    RESULT = []
    for idx, tfile in enumerate(INFO['FILEPATH']):
    
        print tfile.getFilename('utf8'), ":",
        
        for pattern in INFO['PATTERN'].keys():
        
            if( tfile.equalsFirstname(pattern) ):
                
                old_dirpath = tfile.getDirpath('utf8')
                
                new_dirpath = INFO['PATH']['source_directory'].decode( 'utf8' )
                new_filename = INFO['PATTERN'][ pattern ] + "." + tfile.getLastname('utf8')
                INFO['FILEPATH'][idx].renameFilename( new_dirpath, new_filename )
                
                print INFO['FILEPATH'][idx].getFilename('utf8'),
                
                if not os.listdir(old_dirpath):
                    os.rmdir(old_dirpath)
                
                break
                
                
            elif INFO['PATTERN'][pattern] == tfile.getFirstname('utf8'):
                
                old_dirpath = tfile.getDirpath('utf8')
                
                new_dirpath = INFO['PATH']['source_directory'].decode( 'utf8' )
                new_filename = tfile.getFilename('utf8')
                INFO['FILEPATH'][idx].renameFilename( new_dirpath, new_filename )
                
                print INFO['FILEPATH'][idx].getFilename('utf8'),
                
                if not os.listdir(old_dirpath):
                    os.rmdir(old_dirpath)
                
                break
            
        print

        
        
        
    sys.exit()