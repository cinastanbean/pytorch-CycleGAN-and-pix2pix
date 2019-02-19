#!/usr/bin/env bash
set -ex

DATAROOT=./datasets/lookbook

TRAIN_LOG_FILENAME="train_`date +%Y%m%d_%H%M%S`".log
VAL_LOG_FILENAME="val_`date +%Y%m%d_%H%M%S`".log


python train.py --dataroot ${DATAROOT} \
                --name lookbook_pix2pix \
                --model pix2pix \
                --netG unet_256 \
                --batch_size 8 \
                --display_id 10 \
                --direction AtoB \
                --lambda_L1 100 \
                --dataset_mode aligned \
                --norm batch \
                --pool_size 0 \
                2>&1 | tee ${TRAIN_LOG_FILENAME}

echo "Train... Done."