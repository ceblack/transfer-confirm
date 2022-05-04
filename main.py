#!/usr/bin/env python3
import os
import sys
import hashlib
from logging_util import *

# BUF_SIZE is the size of the chunks being read in
# for the hashing function, it's completely arbitrary
BUF_SIZE = 65536

class Comparer:
    def __init__(self, dir_source, dir_dest):
        self.dir_source = dir_source
        self.dir_dest = dir_dest

        logger.info('Source Dir: {}'.format(self.dir_source))
        logger.info('Dest Dir: {}'.format(self.dir_dest))

        self.source_file_paths = []

        self.file_pairs = []

        self.load_source_data()
        self.load_dest_data()
        self.compare_files()

    def load_source_data(self):
        self.source_file_paths = [self.dir_source + x for x in os.listdir(self.dir_source)]
        for p in self.source_file_paths:
            logger.info('Found Source File {}'.format(p))

    def load_dest_data(self):
        source_files = [[x[x.rindex('/') + 1:], x] for x in self.source_file_paths]
        dest_files = os.listdir(self.dir_dest)

        for sf in source_files:
            if sf[0] in dest_files:
                logger.info('File {} found in source dir'.format(sf[0]))
                dest_file_path = self.dir_dest + sf[0]
                self.file_pairs.append([sf[1], dest_file_path])

            else:
                logger.info('MISSING FILE - NOT IN SOURCE DIR: {}'.format(sf[0]))

        logger.info('FILE PAIRS: {}'.format(len(self.file_pairs)))
        logger.info('SOURCE FILES: {}'.format(len(self.source_file_paths)))

    def compare_files(self):
        for pair in self.file_pairs:
            file_path_a = pair[0]
            file_path_b = pair[1]

            file_name_a = file_path_a[file_name_a.rindex('/') + 1:]
            file_name_b = file_path_b[file_name_b.rindex('/') + 1:]

            hash_a = self.hash_file(pair[0])
            hash_b = self.hash_file(pair[1])

            hash_digest_a = hash_a.hexdigest()
            hash_digest_b = hash_b.hexdigest()

            logger.info('MD5 Source File {}: {}'.format(file_name_a, hash_digest_a))
            logger.info('MD5 Dest File {}: {}'.format(file_name_b, hash_digest_b))

            if hash_digest_a == hash_digest_b:
                logger.info('File {} is safely in the dest dir'.format(file_name_a))

            else:
                logger.info('FILE NOT SAFELY IN DEST DIR: {}'.format(file_name_a))

    def hash_file(self, file_path):
        md5 = None
        md5 = hashlib.md5()

        with open(file_path, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break

                md5.update(data)

        return(md5)

def execute(dir_source, dir_dest):
    C = Comparer(dir_source, dir_dest)

if __name__ == '__main__':
    execute(sys.argv[1], sys.argv[2])
