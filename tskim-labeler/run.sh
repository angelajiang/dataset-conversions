# Don't use relative paths

# Explode MP4 into frames
VIDEO_PATH="/Users/angela/src/data/videos/iii/iii-01/vimba_iii_1_2018-3-21_7_scaled.mp4"
EXPLODED_FRAME_PATH="/tmp/frames/exploded"
FRAME_PREFIX="iii-01-7-"
FRAME_NAME_SIZE=8

#rm -r $EXPLODED_FRAME_PATH
#mkdir $EXPLODED_FRAME_PATH
#ffmpeg -i $VIDEO_PATH $EXPLODED_FRAME_PATH"/"$FRAME_PREFIX"%8d.jpg"

# Create Mainstream-format dataset
LABELS_DIR="/Users/angela/src/private/labeler/iii_01_buses/iii_01_7"
LABELS_OUT="/Users/angela/src/private/dataset-conversions/tskim-labeler/labels/iii_01_7.out"
EVENT_LABEL="bus"
NO_EVENT_LABEL="no-bus"
DATASET_DIR="/Users/angela/src/data/image-data/iii-buses"

python make_dataset.py -ld $LABELS_DIR \
                       -lo $LABELS_OUT \
                       -ne $NO_EVENT_LABEL \
                       -e  $EVENT_LABEL \
                       -v  $VIDEO_PATH \
                       -o  $DATASET_DIR \
                       -fd $EXPLODED_FRAME_PATH \
                       -fp $FRAME_PREFIX \
                       -fs $FRAME_NAME_SIZE
