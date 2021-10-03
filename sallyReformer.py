#!/usr/bin/env python

import argparse

import os
import sys

import pandas as pd


def parse_args(args):
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--pattern', help='Path of file whose file name to change is mapped', default='pattern.csv')
    parser.add_argument('-s', '--source-dir', help='Directory containing files to be renamed', default='.')

    return parser.parse_args(args)


def confirm_arguments(args):
    print('You have decided to do the following:')

    if not os.path.isfile(args.pattern):
        print(f"\tThere is no file of pattern: {args.pattern}")
        return False
    print(f"\tPattern-filepath: {args.pattern}")
    
    if not os.path.isdir(args.source_dir):
        print(f"\tThere is no directory of source: {args.source_dir}")
        return False
    print(f"\tSource-directory: {args.source_dir}")

    return True


class Pattern:

    def __init__(self, filepath):
        self._filepath = filepath
        self._patterns = self.load(filepath)


    def load(self, filepath):
        return pd.read_csv(filepath)
    

    def getPattern(self):
        return self._patterns


class Working:

    def __init__(self, dirpath):
        self._dirpath = dirpath


    def change(self, pattern):
        for root, dirs, files in os.walk(self._dirpath):
            for f in files:
                absname = os.path.join(root, f)

                head = f.split('.')[0]
                tail = '.'.join(f.split('.')[1:])

                searched = pattern[pattern['source'] == head]
                if len(searched) != 0:
                    newname = os.path.join(root, '..', f"{searched.iloc[0]['target']}.{tail}")
                    os.rename(absname, newname)
                    os.rmdir(root)
                    print(f"\t{os.path.basename(absname)} -> {os.path.basename(newname)}")


def main(args):
    args = parse_args(args)
    has_confirmed = confirm_arguments(args)

    if has_confirmed:
        pattern = Pattern(args.pattern)
        working = Working(args.source_dir)

        print("Filename changing ...")
        working.change(pattern.getPattern())


if __name__ == '__main__':
    main(sys.argv[1:])