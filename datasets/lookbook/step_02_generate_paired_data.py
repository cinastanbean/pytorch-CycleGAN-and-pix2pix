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

def find_classes(dir):
    classes = [d for d in os.listdir(dir) if os.path.isdir(os.path.join(dir, d))]
    classes.sort()
    class_to_idx = {classes[i]: i for i in range(len(classes))}
    return classes, class_to_idx

def center_paste(img):
    height = img.height
    width = img.width
    maxwh = max(height, width)
    img = img.resize([int(width/maxwh*256), int(height/maxwh*256)])
    val = img.getpixel((1,1))
    image = Image.new(img.mode, [256,256], val)
    box = tuple([int((256-img.width)/2),
                 int((256-img.height)/2),
                 int((256-img.width)/2) + img.width,    # do NOT do -1;
                 int((256-img.height)/2) + img.height])
    image.paste(img, box)
    return image
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='python main.py --path=data_dstfoler')
    parser.add_argument("--path", default='data_dstfoler', type=str)
    args = parser.parse_args()
    path = args.path
    
    '''--------------------------------------'''
    
    dstfoler = path + '_paired'
    mkdir_if_not_exist([dstfoler])
    
    dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

    for d in dirs:
        filelist = get_filelist(os.path.join(path, d))
        file = filelist[0]
        
        
        # A:B = CLEAN0:CLEAN1
        As = []
        Bs = []
        for file in filelist:
            if 'CLEAN0' in file:
                As.append(file)
            elif 'CLEAN1' in file:
                Bs.append(file)
        if len(As)<1 or len(Bs)<1:
            continue
        counter = 1
        for b in Bs:
            imgb = Image.open(b)
            imgb = center_paste(imgb)
            for a in As:
                imga = Image.open(a)
                imga = center_paste(imga)
                imga = imga.convert(imgb.mode)
                image = Image.new(imgb.mode, (512,256))
                image.paste(imga, (0,0,256,256))
                image.paste(imgb, (256,0,512,256))
                paired_filename = d + '_' + str(counter) + '.jpg'
                counter += 1
                image.save(os.path.join(dstfoler, paired_filename))
            
    '''
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
    '''
    
    