#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 11:44:50 2019

Python 3.6.6 |Anaconda, Inc.| (default, Jun 28 2018, 11:07:29)

@author: lisi@meili-inc.com
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import argparse
import shutil
from PIL import Image

# usage: is_allowed_extension(filename, IMG_EXTENSIONS)
IMG_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.ppm', '.bmp', '.pgm', '.tif']
extensions = IMG_EXTENSIONS
def is_allowed_extension(filename, extensions):
    filename_lower = filename.lower()
    return any([filename_lower.endswith(ext) for ext in extensions])

# usage: mkdir_if_not_exist([root, dir])
def mkdir_if_not_exist(path):
    if not os.path.exists(os.path.join(*path)):
        os.makedirs(os.path.join(*path))


# return all type filepath of this path
def get_filelist(path):
    filelist = []
    for root,dirs,filenames in os.walk(path):
        for fn in filenames:
            filelist.append(os.path.join(root,fn))
    return filelist


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='python main.py --path=data')
    parser.add_argument("--path", default='data', type=str)
    args = parser.parse_args()
    path = args.path
    
    '''--------------------------------------'''
    
    dstfoler = path + '_dstfoler'
    mkdir_if_not_exist([dstfoler])
    
    # get filelist
    filelist = get_filelist(path)
    
    # - Image file name: sprintf( 'PID%06d_CLEAN%d_IID%06d', product_id, is_product_image, image_id )
    image_counter = 0
    for filename in filelist:
        if not is_allowed_extension(filename, extensions):
            continue
        # os.path.split(filename)[-1].split('.')[0].split('_') = ['PID004418', 'CLEAN0', 'IID043438']
        keys = os.path.split(filename)[-1].split('.')[0].split('_')
        pid = keys[0]
        isclean = (keys[1] == 'CLEAN1')
        foldername = os.path.join(dstfoler, pid)
        mkdir_if_not_exist([foldername])
        shutil.move(filename, foldername)
    
    
    