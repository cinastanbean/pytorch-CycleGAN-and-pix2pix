#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 14:24:22 2018

@author: pilgrim.bin@163.com
"""

import os
import shutil
import random

import argparse
import threading
from threading import Lock
import math


from PIL import Image


# usage: is_allowed_extension(filename, IMG_EXTENSIONS)
IMG_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.ppm', '.bmp', '.pgm', '.tif']
def is_allowed_extension(filename, extensions):
    filename_lower = filename.lower()
    return any([filename_lower.endswith(ext) for ext in extensions])


# usage: mkdir_if_not_exist([root, dir])
def mkdir_if_not_exist(path):
    if not os.path.exists(os.path.join(*path)):
        os.makedirs(os.path.join(*path))

# usage: is_already_exists(src_file, dstpath)
def is_already_exists(src_file, dstpath):
    filename = os.path.split(src_file)[-1]
    dstfile = os.path.join(dstpath, filename)
    return os.path.exists(dstfile)
        
        
# return all type filepath of this path
def get_filelist(path):
    filelist = []
    for root,dirs,filenames in os.walk(path):
        for fn in filenames:
            filelist.append(os.path.join(root,fn))
    return filelist

def scanning_filelist(filelist):
    extensions = IMG_EXTENSIONS
    for filename in filelist:
        if is_allowed_extension(filename, extensions):
            try:
                img = Image.open(filename)
                img = img.convert('RGB')
            except:
                print("GotShit = {}".format(filename))
                os.remove(filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='python main.py --path=data'
            )
    parser.add_argument(
                        "--path",
                        default='data',
                        type=str,
                        )
    parser.add_argument(
                        "--workers",
                        default=100,
                        type=int,
                        )
    args = parser.parse_args()
    path = args.path
    num_worker = args.workers
    
    '''--------------------------------------'''
    
    # get filelist
    filelist = get_filelist(path)
    random.shuffle(filelist)
    
    # mt
    task_per_worker = int(math.ceil(1. * len(filelist) / num_worker))
    threads = []
    for i in range(num_worker):
        sub_filelist = filelist[i * task_per_worker:(i + 1) * task_per_worker]
        threads.append(
            threading.Thread(target=scanning_filelist, args=([sub_filelist]))
        )
    for i in range(len(threads)):
        threads[i].start()
    for i in range(len(threads)):
        threads[i].join()
        
    print("Done.")
    