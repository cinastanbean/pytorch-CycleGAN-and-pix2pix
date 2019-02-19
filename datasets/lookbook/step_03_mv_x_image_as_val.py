#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 23 15:13:01 2018

@author: pilgrim.bin@163.com
"""

import os
import argparse
import shutil
import random

from PIL import Image

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
    parser = argparse.ArgumentParser(
            description='python main.py --path=datapath'
            )
    parser.add_argument("--srcfolder",
                        default='train',# move max(N*0.2, MAX_MV_NUMBER) samples to dstfolder
                        type=str)
    parser.add_argument("--dstfolder",
                        default='val',
                        type=str)
    parser.add_argument("--phase",
                        default='move',
                        type=str,
                        help='phase = copy or move')
    parser.add_argument("--number",
                        default=3000,
                        type=int)
    args = parser.parse_args()
    
    srcfolder = args.srcfolder
    dstfolder = args.dstfolder
    phase = args.phase
    MAX_MV_NUMBER = args.number
    
    '''--------------------------------------'''

    path = srcfolder
    filelist = get_filelist(path)
    random.shuffle(filelist)
    random.shuffle(filelist)
    random.shuffle(filelist)

    ns = len(filelist)
    split_ratio = 0.2

    # 三选一
    #mv_list = filelist[0:min([MAX_MV_NUMBER, int(split_ratio * ns)])]
    #mv_list = filelist[0:max([MAX_MV_NUMBER, int(split_ratio * ns)])]
    mv_list = filelist[0:MAX_MV_NUMBER]

    if phase == 'copy':
        for filename in mv_list:
            print(filename)
            shutil.copy(filename, dstfolder)
    elif phase == 'move':
        for filename in mv_list:
            print(filename)
            shutil.move(filename, dstfolder)


