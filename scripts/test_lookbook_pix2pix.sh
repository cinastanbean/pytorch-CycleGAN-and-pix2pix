set -ex

DATAROOT=./datasets/lookbook

TRAIN_LOG_FILENAME="train_`date +%Y%m%d_%H%M%S`".log
VAL_LOG_FILENAME="val_`date +%Y%m%d_%H%M%S`".log

python test.py --dataroot ${DATAROOT} \
               --name lookbook_pix2pix \
               --model pix2pix \
               --num_test 1000 \
               --netG unet_256 \
               --direction AtoB \
               --dataset_mode aligned \
               --norm batch \
               2>&1 | tee $VAL_LOG_FILENAME

echo "Val... Done."

