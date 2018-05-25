# Don't use relative paths!
-X

EVENT_LABEL="redcar"
NO_EVENT_LABEL="no-redcar"
DATASET_DIR="/Users/angela/src/data/image-data/iii-redcar"

VIDEO_PATH="/Users/angela/src/data/videos/iii/iii-01/vimba_iii_1_2018-3-21_7_scaled.mp4"
EXPLODED_FRAME_PATH="/Users/angela/src/data/image-data/frames/exploded-7"
FRAME_PREFIX="iii-01-7-"
FRAME_NAME_SIZE=12

mkdir $EXPLODED_FRAME_PATH
ffmpeg -i $VIDEO_PATH $EXPLODED_FRAME_PATH"/"$FRAME_PREFIX"%12d.jpg"

LABELS_DIR="/Users/angela/src/private/labeler/iii_01_redcar/iii_01_7"
LABELS_OUT="/Users/angela/src/private/dataset-conversions/tskim-labeler/labels/iii_01_7.out"

python make_dataset.py -ld $LABELS_DIR \
                       -lo $LABELS_OUT \
                       -ne $NO_EVENT_LABEL \
                       -e  $EVENT_LABEL \
                       -v  $VIDEO_PATH \
                       -o  $DATASET_DIR \
                       -fd $EXPLODED_FRAME_PATH \
                       -fp $FRAME_PREFIX \
                       -fs $FRAME_NAME_SIZE

VIDEO_PATH="/Users/angela/src/data/videos/iii/iii-01/scaled_vimba_iii_1_2018-3-21_16.mp4"
EXPLODED_FRAME_PATH="/Users/angela/src/data/image-data/frames/exploded-16"
FRAME_PREFIX="iii-01-16-"
FRAME_NAME_SIZE=12

mkdir $EXPLODED_FRAME_PATH
ffmpeg -i $VIDEO_PATH $EXPLODED_FRAME_PATH"/"$FRAME_PREFIX"%12d.jpg"

LABELS_DIR="/Users/angela/src/private/labeler/iii_01_redcar/iii_01_16"
LABELS_OUT="/Users/angela/src/private/dataset-conversions/tskim-labeler/labels/iii_01_16.out"

python make_dataset.py -ld $LABELS_DIR \
                       -lo $LABELS_OUT \
                       -ne $NO_EVENT_LABEL \
                       -e  $EVENT_LABEL \
                       -v  $VIDEO_PATH \
                       -o  $DATASET_DIR \
                       -fd $EXPLODED_FRAME_PATH \
                       -fp $FRAME_PREFIX \
                       -fs $FRAME_NAME_SIZE

